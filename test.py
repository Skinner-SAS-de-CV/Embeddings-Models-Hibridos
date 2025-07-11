from evaluador import evaluador

# Prueba de neutralidad (género/edad)
cvs_neutrales = [
    "Experiencia en Python y SQL, 5 años en Amazon",
    "Tengo 10 años de experiencia en Java y Spring",
    "Soy desarrollador Fullstack con Node y React",
    "Soy desarrolladora Frontend con Angular"
]

print("🔍 Iniciando pruebas de sesgo...")
for cv in cvs_neutrales:
    resultado = evaluador(cv, "Desarrollador Senior", ["Java", "Python", "React", "Angular"])
    print(f"\nCV: {cv[:50]}...")
    print(f" Puntuación total: {resultado['puntuacion']}/10")
    print(f" Habilidades detectadas: {', '.join([h[0] for h in resultado['detalles']['habilidades_detectadas']])}")
    print(f" Scores: MiniLM={resultado['detalles']['all_mini_score']}, Spanish={resultado['detalles']['spanish_model_score']}")