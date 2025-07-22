from datetime import datetime
import os
from typing import List, Optional
import uvicorn
import PyPDF2
import docx2txt
import re
import dill
import joblib
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from openai import AsyncOpenAI
from dotenv import load_dotenv
from funciones import extraer_habilidades_responsabilidades 
import asyncio

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("ERROR: La API Key de OpenAI no se encontró.")

async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Carga del Sistema Guardado
# ----------------------------
try:
    with open('modelos_skinner/sistema_evaluacion_cv.joblib', 'rb') as f:
        sistema = dill.load(f)
    print("Sistema de evaluación cargado correctamente")
    
    if 'funcion_habilidades' not in sistema:
        from funciones import extraer_habilidades_responsabilidades
        sistema['funcion_habilidades'] = extraer_habilidades_responsabilidades

    model_mini = sistema['model_mini']
    model_spanish = sistema['model_spanish']
    clasificador = sistema['clasificador']
    evaluar_candidato = sistema['funcion_evaluar']  # Función de evaluación calibrada
    df_puestos = sistema['df_puestos']
    config = sistema['configuracion']
    
    print(f"Sistema guardado el: {config['fecha_guardado']}")
    print(f"Pesos configurados: {config['pesos']}")
    print(f"Habilidades cargadas para {len(df_puestos)} puestos")
    
except FileNotFoundError:
    print("Error: No se encontró el archivo del modelo")
    raise
except Exception as e:
    print(f"Error cargando el sistema: {str(e)}")
    raise RuntimeError("No se pudo cargar el sistema de evaluación") from e

# ----------------------------
# Funciones Clave
# ----------------------------

def extract_text(file: UploadFile) -> str:
    """Extrae texto de PDF o DOCX"""
    text = ""
    if file.filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = " ".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    elif file.filename.endswith(".docx"):
        text = docx2txt.process(file.file)
    return text

async def match_resume_to_job(resume_text: str, job_desc: str, habilidades: list) -> dict:
    """Usa el sistema guardado para evaluar el CV"""
    try:
        # Usamos la función de evaluación del sistema guardado
        resultado = evaluar_candidato(
            cv_text=resume_text,
            descripcion_puesto=job_desc,
            habilidades_clave=habilidades
        )
        
        # Convertimos las habilidades detectadas a un formato serializable
        habilidades_detectadas = [
            {"habilidad": h[0], "puntuacion": float(h[1])} 
            for h in resultado["detalles"]["habilidades_detectadas"]
        ]
        
        return {
            "puntuacion_cruda": resultado["puntuacion_cruda"],
            "puntuacion_calibrada": resultado["puntuacion_calibrada"],
            "categoria": resultado["categoria"],
            "detalles": {
                "mini_score": resultado["detalles"]["mini_score"],
                "spanish_score": resultado["detalles"]["spanish_score"],
                "habilidades_score": resultado["detalles"]["habilidades_score"],
                "habilidades_detectadas": habilidades_detectadas
            }
        }
        
    except Exception as e:
        print(f"Error en evaluación: {str(e)}")
        # Agrega más detalles al error para diagnóstico
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Error en evaluación: {str(e)}"
        ) from e

async def generate_gpt_feedback(texto_cv: str, tipo_de_trabajo: str, descripcion_del_trabajo: str) -> str:
    prompt = f"""
    Eres un experto en recursos humanos. Analiza el siguiente CV para el puesto: {tipo_de_trabajo}
    
    **CONTENIDO DEL CV:**
    {texto_cv[:10000]}  # Limita a 10,000 caracteres por seguridad

    **DESCRIPCIÓN DEL PUESTO:**
    {descripcion_del_trabajo}

    **TAREAS:**
    - Resume puntos fuertes/debiles basado EXCLUSIVAMENTE en el CV
    - Compara las habilidades del CV con: {descripcion_del_trabajo}
    - Analiza cumplimiento de funciones/requisitos con : {descripcion_del_trabajo}
    - Recomendación final basada en datos concretos
    
    **FORMATO:**
    - Puntos Fuertes: [Menciona habilidades específicas del CV]
    - Puntos Débiles: [Falta de habilidades requeridas]
    - Cumplimiento: [% de coincidencia con el puesto]
    - Recomendación: [Fundamentada en el análisis]
    
    IMPORTANTE: 
    - Solo menciona habilidades/experiencia EXPLÍCITAS en el CV. 
    - Nunca asumas o inferas información no escrita.
    """
    
    try:
        response = await async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en selección de talento humano."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # temperatura controla la creatividad
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error en GPT: {str(e)}")
        return "Error generando feedback"

# ----------------------------
# Endpoint Principal
# ----------------------------

@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...),
    tipo_de_trabajo: str = Form(...),
    descripcion_del_trabajo: str = Form(...),
    habilidades: str = Form(...),
    nombre_candidato: str = Form(...)
):
    # Extraer texto del CV
    cv_text = extract_text(file)
    
    # Convertir habilidades a lista
    habilidades_lista = [h.strip() for h in habilidades.split(",")] if habilidades else []
    
    # Evaluar coincidencia y generar feedback en paralelo
    match_task = asyncio.create_task(
        match_resume_to_job(cv_text, descripcion_del_trabajo, habilidades_lista))
    feedback_task = asyncio.create_task(
        generate_gpt_feedback(cv_text, tipo_de_trabajo, descripcion_del_trabajo))
    
    match_result, feedback = await asyncio.gather(match_task, feedback_task)
    
    # Respuesta estructurada usando la categoría ya calculada
    return {
        "candidate": nombre_candidato,
        "job": tipo_de_trabajo,
        "puntuacion_cruda": match_result["puntuacion_cruda"],
        "puntuacion_calibrada": match_result["puntuacion_calibrada"],
        "decision": match_result["categoria"],  # Usamos la categoría ya calculada
        "feedback": feedback,
        "details": match_result["detalles"],
        "config": {
            "pesos": config['pesos'],
            "umbral_habilidades": config['umbral_habilidades']
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)