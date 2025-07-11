import os
import re
import pandas as pd
import pdfplumber
import tabula
from tqdm import tqdm

INPUT_DIR = "pdf_candidatos"
OUTPUT_DIR = "csvs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Patrones regex para CVs
PATRONES = {
    "Nombre de Candidato": re.compile(r"(?i)(?:nombre\s*(?:del\s*)?candidato\s*[:\-]\s*)(.+?)(?=\n|$)", re.DOTALL),
    "Puesto evaluado": re.compile(r"(?i)(?:puesto\s*(?:de\s*)?evaluado\s*[:\-]\s*)(.+?)(?=\n|$)", re.DOTALL),
    "calificacion": re.compile(r"(?i)calificaci[oó]n\s*[:\-]\s*(.+?)(?=\n\w+:|$)", re.DOTALL),
    "decision": re.compile(r"(?i)decisi[oó]n\s*(?:final\s*)?[:\-]\s*(.+?)(?=\n|$)", re.DOTALL),
}

def extraer_texto_estructurado(texto):
    datos = {}
    print("\n🔍 Analizando texto...")  # Debug
    
    for campo, patron in PATRONES.items():
        match = patron.search(texto)
        if match:
            valor = match.group(1).strip()
            # Limpieza adicional de espacios/tabulaciones
            valor = ' '.join(valor.split()) 
            datos[campo] = valor
            print(f" {campo}: {valor}") 
        else:
            datos[campo] = None
            print(f"No se encontró: {campo}")  
            print(f"Texto relevante:\n{texto[:500]}...")  
    
    return datos

def procesar_pdf(pdf_path):
    try:
        texto_completo = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                texto_completo += page.extract_text() + "\n\n"
        
        datos_texto = extraer_texto_estructurado(texto_completo)
        tablas = tabula.read_pdf(
            pdf_path,
            pages="all",
            multiple_tables=True,
            lattice=True,
            silent=True
        )
        
    
        datos_tablas = {}
        if tablas:
            df_tablas = pd.concat(tablas, ignore_index=True)
            datos_tablas = {"tablas": len(tablas), "filas_totales": len(df_tablas)}
            # Guardar tablas en CSV aparte
            nombre_tablas_csv = os.path.join(OUTPUT_DIR, os.path.basename(pdf_path).replace(".pdf", "_TABLAS.csv"))
            df_tablas.to_csv(nombre_tablas_csv, index=False, encoding="utf-8-sig")
        
        datos_completos = {**datos_texto, **datos_tablas, "texto_completo": texto_completo}
        df_final = pd.DataFrame([datos_completos])
        
        nombre_csv = os.path.join(OUTPUT_DIR, os.path.basename(pdf_path).replace(".pdf", ".csv"))
        df_final.to_csv(nombre_csv, index=False, encoding="utf-8-sig")
        
        return nombre_csv
    
    except Exception as e:
        print(f"Error procesando {pdf_path}: {str(e)}")
        return None

print(f"Buscando PDFs en '{INPUT_DIR}'...")
pdfs = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

if not pdfs:
    print("No se encontraron archivos PDF.")
else:
    print(f"Procesando {len(pdfs)} archivos...")
    exitosos = 0
    for pdf in tqdm(pdfs, desc="Progreso"):
        if procesar_pdf(pdf):
            exitosos += 1
    
    print(f"\n{exitosos}/{len(pdfs)} archivos convertidos en '{OUTPUT_DIR}'.")

consolidar = input("¿Consolidar todos los CSVs en un único archivo? (s/n): ").lower() == "s"
if consolidar:
    dfs = []
    for csv in os.listdir(OUTPUT_DIR):
        if csv.endswith(".csv") and not csv.endswith("_TABLAS.csv"):
            dfs.append(pd.read_csv(os.path.join(OUTPUT_DIR, csv)))
    
    if dfs:
        pd.concat(dfs, ignore_index=True).to_csv("csvs_final.csv", index=False)
        print("Archivo 'csvs_final.csv' creado.")