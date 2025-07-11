from datetime import datetime
import os
from typing import List, Optional
import uvicorn
import PyPDF2
import docx2txt
import re
from fastapi import FastAPI, UploadFile, File, Form, Depends, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from openai import AsyncOpenAI
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import smtplib
from email.message import EmailMessage
from pydantic import BaseModel, EmailStr, field_validator
import bleach
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json

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
# Carga de Modelos
# ----------------------------

model_mini = SentenceTransformer('modelos_skinner/all_mini_model')
model_spanish = SentenceTransformer('modelos_skinner/spanish_model')
clasificador = pipeline(
    "zero-shot-classification",
    model="modelos_skinner/zero_shot_classifier",
    device="cpu"
)

# ----------------------------
# Funciones Clave Mejoradas
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

def match_resume_to_job(resume_text: str, job_desc: str, habilidades: list) -> dict:
    """Nueva función de matching con modelos mejorados"""
    # Embeddings con ambos modelos
    emb_mini_cv = model_mini.encode(resume_text)
    emb_mini_job = model_mini.encode(job_desc)
    sim_mini = util.cos_sim(emb_mini_job, emb_mini_cv).item()
    
    emb_spanish_cv = model_spanish.encode(resume_text)
    emb_spanish_job = model_spanish.encode(job_desc)
    sim_spanish = util.cos_sim(emb_spanish_job, emb_spanish_cv).item()
    
    # Detección de habilidades
    if habilidades:
        resultados_hab = clasificador(
            resume_text,
            candidate_labels=habilidades,
            multi_label=True
        )
        puntaje_habilidades = sum(
            score * 2.5
            for score in resultados_hab['scores']
            if score > 0.7
        )
        habilidades_detectadas = [
            (label, round(score, 2))
            for label, score in zip(resultados_hab['labels'], resultados_hab['scores'])
            if score > 0.7
        ]
    else:
        puntaje_habilidades = 0
        habilidades_detectadas = []
    puntuacion = (sim_mini * 4 + sim_spanish * 4 + puntaje_habilidades * 2) * 1.25
    
    return {
        "puntuacion": round(puntuacion, 1),
        "detalles": {
            "all_mini_score": round(sim_mini * 10, 1),
            "spanish_model_score": round(sim_spanish * 10, 1),
            "habilidades_detectadas": habilidades_detectadas
        }
    }

async def generate_gpt_feedback(texto_cv: str, tipo_de_trabajo: str, descripcion_del_trabajo: str) -> str:
    prompt = f"""
    Eres un experto en recursos humanos. Analiza el siguiente CV para el puesto: {tipo_de_trabajo}
    - Analisa el **{texto_cv}** si cumple con las habilidades del puesto de trabajo.
    -Analisa si el candidato cumple con la **{descripcion_del_trabajo}**.
    
    Descripción del puesto:
    {descripcion_del_trabajo}
    
    CV del candidato:
    {texto_cv[:5000]}... [truncado]
    
    **Tareas a realizar:**
    - Resume los puntos fuertes y débiles del candidato.
    - Explica si tiene las habilidades requeridas o no.
    - Analiza si cumple con las funciones y requisitos del cliente.
    - Da una recomendación final sobre si el candidato es adecuado para el puesto segun con la calificación.

    ** Formato de respuesta esperado:**
    - **Puntos Fuertes:** 
    - **Puntos Débiles:** 
    - **Cumplimiento con el perfil:** 
    - **Recomendación final:**
    """
    
    response = await async_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un experto en selección de talento humano."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

# ----------------------------
# Endpoint Principal Mejorado
# ----------------------------

@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...),
    tipo_de_trabajo: str = Form(...),
    descripcion_del_trabajo: str = Form(...),
    habilidades: str = Form(...),
    nombre_candidato: str = Form(...)
):
    texto_cv = extract_text(file)
    
    # Convertir habilidades a lista
    habilidades_lista = [h.strip() for h in habilidades.split(",")] if habilidades else []
    
    match_task = asyncio.to_thread(
        match_resume_to_job, 
        texto_cv, 
        descripcion_del_trabajo,
        habilidades_lista
    )
    feedback_task = generate_gpt_feedback(texto_cv, tipo_de_trabajo, descripcion_del_trabajo)
    
    match_result, feedback = await asyncio.gather(match_task, feedback_task)
    
    # Determinar decisión
    if match_result["puntuacion"] >= 8.0:
        calificacion = "Alto"
    elif match_result["puntuacion"] >= 6.0:
        calificacion = "Moderado"
    else:
        calificacion = "Bajo"
    
    return {
        "candidate": nombre_candidato,
        "job": tipo_de_trabajo,
        "calificacion": match_result["puntuacion"],
        "decision": calificacion,
        "feedback": feedback,
        "details": match_result["detalles"]
    }

# ----------------------------
# Endpoint de Prueba Rápida no es necesario tenerlo pero para pruebas rápidas esta super útil.
# ----------------------------

@app.post("/quick_test/")
async def quick_test(
    file: UploadFile = File(...),
    tipo_de_trabajo: str = Form(...),
    descripcion_del_trabajo: str = Form(...),
    habilidades: str = Form("")
):
    """Endpoint simplificado para pruebas rápidas"""
    habilidades_lista = [h.strip() for h in habilidades.split(",")] if habilidades else []
    resume_text = extract_text(file)
    
    match_result = await asyncio.to_thread(
        match_resume_to_job,  
        resume_text,
        descripcion_del_trabajo,
        habilidades_lista
    )
    
    return {
        "job": tipo_de_trabajo,
        "match_score": match_result["puntuacion"],
        "details": match_result["detalles"]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)