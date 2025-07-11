from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# Cargar modelos (fuera de la función para que solo se carguen una vez)
model_mini = SentenceTransformer('./modelos_skinner/all_mini_model')
model_spanish = SentenceTransformer('./modelos_skinner/spanish_model')
clasificador = pipeline("zero-shot-classification", model="./modelos_skinner/zero_shot_classifier")

def evaluador(cv_text, job_desc, habilidades):
    # Embeddings y similitud
    emb_mini_cv = model_mini.encode(cv_text)
    emb_mini_job = model_mini.encode(job_desc)
    sim_mini = util.cos_sim(emb_mini_job, emb_mini_cv).item()

    emb_spanish_cv = model_spanish.encode(cv_text)
    emb_spanish_job = model_spanish.encode(job_desc)
    sim_spanish = util.cos_sim(emb_spanish_job, emb_spanish_cv).item()

    # Habilidades con zero-shot
    if habilidades:
        resultados_hab = clasificador(
            cv_text,
            candidate_labels=habilidades,
            multi_label=True
        )
        habilidades_detectadas = [
            (label, round(score, 2)) 
            for label, score in zip(resultados_hab['labels'], resultados_hab['scores']) 
            if score > 0.7
        ]
        puntaje_habilidades = sum(score for score in resultados_hab['scores'] if score > 0.7)
    else:
        habilidades_detectadas = []
        puntaje_habilidades = 0
    # Calcular puntuación final
    puntuacion = (sim_mini * 4 + sim_spanish * 4 + puntaje_habilidades * 2) * 1.25

    return {
        "puntuacion": round(puntuacion, 1),
        "detalles": {
            "all_mini_score": round(sim_mini * 10, 1),
            "spanish_model_score": round(sim_spanish * 10, 1),
            "habilidades_detectadas": habilidades_detectadas
        }
    }

if __name__ == "__main__":
    ejemplo = evaluador(
        "Experiencia en Python y Django",
        "Desarrollador Backend Senior",
        ["Python", "Django", "SQL"]
    )
    print(ejemplo)