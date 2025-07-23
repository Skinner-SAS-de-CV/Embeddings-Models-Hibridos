import csv
import random
from faker import Faker

# Inicializar Faker para generar datos en español
fake = Faker('es_ES')

# --- Listas de Datos para Generación Aleatoria ---

# Habilidades
habilidades_tecnicas = [
    "Python", "Java", "C++", "JavaScript", "SQL", "Big Data", "Machine Learning",
    "Inteligencia Artificial", "Análisis de Datos", "Microsoft Azure", "AWS",
    "Google Cloud Platform", "Scrum", "Agile", "Gestión de Proyectos", "SAP",
    "Ciberseguridad", "Bases de Datos NoSQL", "DevOps", "Docker", "Kubernetes",
    "React", "Angular", "Vue.js", "Node.js", "Diseño UX/UI", "Figma", "Sketch","NIIF",
    "USGAAP","NIC","ACL","IDEA","TeamMate,","Power BI", "Tableau", "Excel Avanzado", "R", "MATLAB",
    "Oracle Financials", "Salesforce", "SAP ERP", "Microsoft Dynamics 365",
    "Blockchain", "Internet de las Cosas (IoT)", "Realidad Aumentada (AR)",
    "Realidad Virtual (VR)", "Automatización de Procesos Robóticos (RPA)",
    "Salesforce","Zendesk","HubSpot","LiveChat"," Intercom","Microsoft Teams",
    "NPS (Net Promoter Score)","Freshdesk","ServiceNow","Dialogflow","Laparoscopia",
    "microcirugía","suturas avanzadas","Interpretación de RX","TAC","RMN","ecografías",
    "Epic","Cerner","historias clínicas electrónicas (HCE)","RCP avanzada","manejo de vía aérea",
    "Dosificación","interacciones medicamentosas","Westlaw","LexisNexis","Google Scholar","Contratos",
    "recursos de apelación","demandas","Manejo de juicios orales","técnicas de interrogatorio",
    "Derecho penal","laboral","fiscal","corporativo","Técnicas de negociación legal","Scanner OBD2","Autel",
    "Launch Tech","Desarme","torqueado","ajuste de válvulas","Baterías","motores eléctricos","MIG","TIG","soldadura en aluminio"
    "Interpretación de diagramas eléctricos y manuales OEM","Uso de GPS (FMS)","cartas aeronáuticas (Jeppesen)"," Interpretación de METAR",
    "SIGMET","radar meteorológico","X-Plane","Prepar3D","entrenamiento en Full Flight Simulator (FFS)","Fallas de motor","despresurización","fuego en cabina",
    "OACI","FAA","EASA","Estratigrafía","uso de palustres","tamizado","Carbono-14","termoluminiscencia","GIS (ArcGIS, QGIS)","photogrametría (Agisoft)","Identificación de restos humanos",
    "Técnicas de limpieza y restauración","Drones","sensores NDVI","tractores autónomos","Análisis de pH","textura","nutrientes (N-P-K)","Cultivos transgénicos",
    "micropropagación","Sistemas de goteo","pivote central","Agroptima","FarmLogs","High-key","low-key","Rembrandt lighting","Photoshop (capas, máscaras)",
    "Lightroom (revelado RAW, ajustes de color)","Técnicas de composición fotográfica","Fotografía de retrato","paisaje","macro","Fotografía de producto",
    "Drone (DJI), 360°","time-lapse","Manejo de perfiles de color","calibración de pantallas","Uso de flashes externos","lentes Tilt-Shift","Revit",
    "AutoCAD","SketchUp","BIM (Building Information Modeling)","Análisis estructural (SAP2000, ETABS)","Diseño de interiores (3ds Max, V-Ray)",
    "Google Analytics","Shopify","WooCommerce","Amazon Seller","Facebook Ads","Google Ads",
]
habilidades_blandas = [
    "Comunicación Efectiva", "Trabajo en Equipo", "Resolución de Problemas",
    "Liderazgo", "Adaptabilidad", "Pensamiento Crítico", "Creatividad",

    "Gestión del Tiempo", "Inteligencia Emocional", "Negociación", "Persuasión","Pensamiento crítico y analítico",
    "Ética profesional","Comunicación asertiva","Tolerancia a la presión","Negociación y resolución de conflictos","Empatía",
    "Paciencia","Adaptabilidad","Resiliencia","Persuasión","Inteligencia emocional","Trabajo en equipo","Paciencia y tacto","Toma de decisiones bajo presión",
    "Liderazgo","Persuasión y oratoria","Negociación","Escucha activa","Resolución de conflictos","Discreción",""
]

# Puestos de Trabajo
puestos_trabajo = [
    "Desarrollador de Software", "Ingeniero de Datos", "Científico de Datos",
    "Analista de Negocios", "Jefe de Proyecto", "Gerente de Producto",
    "Especialista en Marketing Digital", "Diseñador Gráfico", "Analista Financiero",
    "Contador", "Especialista en Recursos Humanos", "Arquitecto de Soluciones Cloud",
    "Auditor / Auditor Financiero","Vendedor Técnico", "Especialista en Ciberseguridad",
    "Administrador de Sistemas", "Ingeniero de Redes", "Consultor de TI","Agronomo",
    "Médico General", "Enfermero", "Abogado", "Piloto de Aerolínea",
    "Técnico de Mantenimiento", "Fotógrafo Profesional",
    "Ingeniero Civil", "Arquitecto", "Técnico de Soporte Informático",
    "Especialista en SEO", "Desarrollador Frontend", "Desarrollador Backend",
    "Ingeniero de Software", "Especialista en Inteligencia Artificial", "Gerente de Proyectos IT",
    "Especialista en Blockchain", "Ingeniero de Seguridad Informática",
    "Especialista en Experiencia del Usuario (UX)", "Gerente de Ventas",
    "Especialista en Atención al Cliente", "Consultor de Transformación Digital","Piloto de Drones",
    "Técnico de Reparación de Electrónica", "Especialista en Logística",
    "Ingeniero Mecánico", "Ingeniero Eléctrico", "Especialista en Energías Renovables",
    "Técnico de Laboratorio", "Especialista en Biotecnología", "Investigador Científico",
    "Especialista en Salud Pública", "Técnico de Radiología",
    "Especialista en Terapia Física", "Psicólogo Clínico", "Nutricionista",
    "Especialista en Medicina Deportiva", "Técnico de Farmacia",
    "Especialista en Odontología", "Veterinario", "Técnico de Mantenimiento de Aeronaves",
    "Piloto de Helicóptero", "Técnico de Mantenimiento de Helicópteros",
    "Ingeniero Aeroespacial", "Especialista en Robótica", "Técnico de Automatización Industrial",
    "Especialista en Internet de las Cosas (IoT)", "Ingeniero de Sistemas Embebidos",
    "Especialista en Realidad Aumentada (AR)", "Especialista en Realidad Virtual (VR)",
    "Especialista en Automatización de Procesos Robóticos (RPA)", "Especialista en Desarrollo de Videojuegos",
    "Especialista en E-commerce", "Especialista en Marketing de Contenidos",
    "Especialista en Publicidad Digital", "Especialista en Redes Sociales",
    "Especialista en Email Marketing", "Especialista en Analítica Web",
    "Especialista en Gestión de Proyectos Ágiles", "Scrum Master", "Product Owner",
    "Especialista en Gestión de Cambio", "Especialista en Innovación y Desarrollo",
    "Especialista en Desarrollo Sostenible", "Especialista en Responsabilidad Social Empresarial (RSE)",
    "Especialista en Compliance", "Especialista en Gestión de Riesgos",
    "Especialista en Auditoría Interna", "Especialista en Control de Calidad",
    "Especialista en Seguridad Industrial", "Especialista en Salud Ocupacional",
    "Especialista en Medio Ambiente", "Especialista en Gestión de Proyectos de Construcción",
    "Especialista en Gestión de Proyectos de Infraestructura", "Especialista en Gestión de Proyectos de Energía",
    "Especialista en Gestión de Proyectos de Tecnología de la Información (TI)", "Especialista en Gestión de Proyectos de Investigación y Desarrollo (I+D)",
]

# Certificaciones
certificaciones = [
    "Scrum Master Certified (SMC)", "Project Management Professional (PMP)",
    "AWS Certified Solutions Architect", "Google Certified Professional Data Engineer",
    "Microsoft Certified: Azure Fundamentals", "Certified Information Systems Security Professional (CISSP)",
    "Cisco Certified Network Associate (CCNA)", "Oracle Certified Professional",
    "Salesforce Certified Administrator", "Google Analytics Individual Qualification (IQ)","Google Professional Machine Learning Engineer",
    "Microsoft Certified: Azure Administrator Associate","Certified Cloud Security Professional (CCSP) (ISC²)","Certified Ethical Hacker (CEH)",
    "Advanced Cardiac Life Support (ACLS)","Board Certification in Surgery (American Board of Surgery)","Certified Medical-Surgical Registered Nurse (CMSRN)",
    "Certified Information Privacy Professional (CIPP)","Certified Compliance & Ethics Professional (CCEP)","Certified Public Accountant (CPA)",
    "Professional in Human Resources (PHR)","SHRM Certified Professional (SHRM-CP)",
]

# Intereses
intereses = [
    "Lectura de blogs de tecnología", "Participación en hackathons", "Contribuciones a proyectos de código abierto",
    "Ajedrez", "Senderismo", "Fotografía", "Running", "Voluntariado en ONGs",
    "Creación de contenido digital", "Inversiones y finanzas personales", "Yoga y meditación"
]

# Funciones Principales de Puestos
funciones_puesto = {
    "Desarrollador de Software": [
        "Diseñar, codificar y depurar aplicaciones de software.",
        "Colaborar con equipos multifuncionales para definir y enviar nuevas funciones.",
        "Mantener la calidad y la capacidad de respuesta de las aplicaciones.",
        "Participar en revisiones de código y compartir las mejores prácticas."
    ],
    "Ingeniero de Datos": [
        "Construir y mantener pipelines de datos escalables.",
        "Diseñar e implementar modelos de datos para el análisis.",
        "Asegurar la integridad y calidad de los datos.",
        "Trabajar con grandes volúmenes de datos estructurados y no estructurados."
    ],
    "Jefe de Proyecto": [
        "Planificar, ejecutar y supervisar proyectos de principio a fin.",
        "Gestionar el alcance, el presupuesto y el cronograma del proyecto.",
        "Coordinar a los miembros del equipo y a las partes interesadas.",
        "Identificar y mitigar los riesgos del proyecto."
    ],
    "Auditor / Auditor Financiero": [
        "Inspeccionar estados financieros para detectar errores, fraudes o declaraciones erróneas",
        "Realizar auditorías de sistemas, operaciones y cuentas, evaluando el cumplimiento normativo (ej. GAAP, NIIF)",
        "Elaborar informes con hallazgos y recomendaciones para mejorar procesos",
        "Evaluar riesgos y controles internos, incluyendo áreas no financieras como TI o seguridad",
        "Investigar irregularidades a solicitud de reguladores o la empresa",
    ],
    "Servicio al Cliente": [
        "Resolver dudas y problemas de clientes mediante múltiples canales (teléfono, chat, email)",
        "Gestionar quejas y reclamos, escalando casos complejos a coordinadores",
        "Recopilar feedback para mejorar la experiencia del cliente",
        "Promover ventas cruzadas o recomendaciones de productos",
        "Mantener registros de interacciones y métricas de satisfacción (ej. CSAT, NPS)"
    ],
    "Doctor Cirujano / Doctor General": [
        "Diagnosticar y tratar enfermedades mediante cirugía o métodos clínicos",
        "Realizar procedimientos quirúrgicos, asegurando esterilidad y seguimiento de protocolos",
        "Coordinar equipos médicos (enfermeros, anestesistas) en quirófanos",
        "Brindar cuidados postoperatorios y educar a pacientes sobre riesgos y recuperación",
        "Mantener historiales clínicos y documentar procedimientos"
    ],
    "Abogado": [
        "Asesorar legalmente a clientes en áreas como penal, laboral o corporativo",
        "Representar clientes en juicios, presentando pruebas y argumentos",
        "Redactar documentos legales (contratos, demandas, testamentos)",
        "Negociar acuerdos extrajudiciales o mediaciones",
        "Investigar jurisprudencia y actualizarse en cambios legislativos"
    ],
    "Mecánico": [
        "Diagnosticar fallas en motores, sistemas eléctricos o hidráulicos",
        "Reparar y mantener vehículos o maquinaria, usando herramientas especializadas",
        "Realizar pruebas de funcionamiento post-reparación",
        "Asesorar a clientes sobre mantenimiento preventivo",
        "Gestionar inventario de repuestos y lubricantes"
    ],
    "Piloto de Avión": [
        "Planificar rutas considerando clima, combustible y aeropuertos",
        "Realizar chequeos pre-vuelo (instrumentos, fuselaje, carga)",
        "Operar aeronaves siguiendo protocolos de seguridad y comunicación con torres",
        "Manejar emergencias (ej. fallas técnicas, turbulencias)",
        "Documentar incidencias y reportar al equipo técnico post-vuelo"
    ],
    "Arqueólogo / Antropólogo" :[
        "Excavar y analizar artefactos en sitios históricos",
        "Estudiar culturas antiguas mediante análisis de restos humanos o estructuras",
        "Usar tecnología como GIS o drones para mapear yacimientos",
        "Publicar hallazgos en informes académicos o museos"
    ],
    "Ingeniero Agrónomo" : [
        "Optimizar cultivos mediante estudios de suelo, riego y fertilizantes",
        "Diseñar sistemas agrícolas sostenibles (ej. energía solar, maquinaria eficiente)",
        "Controlar plagas y enfermedades en plantas o animales",
        "Asesorar a agricultores en técnicas de producción y comercialización"
    ],
    "Fotógrafo" : [
        "Capturar imágenes en sesiones (retratos, eventos, productos) [citation:N/A]",
        "Editar fotos con software como Photoshop o Lightroom [citation:N/A]",
        "Gestionar equipo técnico (cámaras, iluminación, drones) [citation:N/A]"
    ],
    "Arquitecto" : [
        "Diseñar planos con herramientas como AutoCAD o Revit [citation:N/A]",
        "Supervisar construcciones para cumplir normativas [citation:N/A]"
    ]
    
    
}

# Beneficios
beneficios = [
    "Seguro de gastos médicos mayores y menores", "Vales de despensa", "Fondo de ahorro",
    "Trabajo remoto/híbrido", "Horario flexible", "Días de vacaciones superiores a la ley",
    "Bonos por desempeño", "Plan de desarrollo y capacitación continua",
    "Subsidio para gimnasio o actividades de bienestar", "Seguro de vida"
]

# --- Funciones de Generación ---

def generar_cv():
    """Genera una cadena de texto con el formato de un CV detallado."""
    edad = random.randint(22, 60)
    nombre_puesto = random.choice(puestos_trabajo)
    experiencia = f"""
- **{nombre_puesto}** en {fake.company()} ({random.randint(2, 6)} años)
  - Responsable de {random.choice(funciones_puesto.get(nombre_puesto, ["tareas genéricas"]))}.
  - Logré un {random.choice(['aumento del 15% en la eficiencia', 'reducción del 20% en costos operativos', 'mejora del 25% en la satisfacción del cliente'])}.
- **{random.choice(puestos_trabajo)} Jr.** en {fake.company()} ({random.randint(1, 3)} años)
  - Apoyo en el desarrollo y mantenimiento de sistemas.
"""
    cv = f"""**Candidato:** {fake.name()}
**Edad:** {edad} años

**Resumen Profesional:**
Profesional con más de {random.randint(5, 15)} años de experiencia en el sector tecnológico, especializado en {nombre_puesto}. Busco aplicar mis habilidades para impulsar la innovación y el crecimiento.

**Experiencia Laboral:**
{experiencia}
**Habilidades Técnicas:**
- {', '.join(random.sample(habilidades_tecnicas, k=random.randint(4, 7)))}

**Habilidades Blandas:**
- {', '.join(random.sample(habilidades_blandas, k=random.randint(3, 5)))}

**Certificaciones:**
- {random.choice(certificaciones)}
- {random.choice(certificaciones)}

**Intereses:**
- {', '.join(random.sample(intereses, k=random.randint(2, 4)))}
"""
    return cv

def generar_descripcion_puesto():
    """Genera una cadena de texto con el formato de una descripción de puesto detallada."""
    nombre_puesto = random.choice(puestos_trabajo)
    desc = f"""**Puesto:** {nombre_puesto}
**Empresa:** {fake.company()}
**Ubicación:** {fake.city()}, {random.choice(['Modalidad Híbrida', 'Remoto', 'Presencial'])}

**Descripción General:**
Buscamos un {nombre_puesto} apasionado y proactivo para unirse a nuestro equipo dinámico. Serás responsable de liderar iniciativas clave y contribuir al éxito de nuestros productos.

**Funciones Principales:**
- {'. '.join(random.sample(funciones_puesto.get(nombre_puesto, ["Realizar tareas asignadas por el gerente."]), k=min(3, len(funciones_puesto.get(nombre_puesto, [])))))}
- Colaborar estrechamente con los departamentos de Producto, Diseño y Marketing.
- Analizar datos para proponer mejoras continuas.

**Requisitos:**
- Titulación universitaria en Informática, Ingeniería o campo relacionado.
- Mínimo {random.randint(3, 7)} años de experiencia en un rol similar.
- Experiencia demostrable en: {', '.join(random.sample(habilidades_tecnicas, k=3))}.
- Excelentes habilidades de: {', '.join(random.sample(habilidades_blandas, k=2))}.
- Nivel de inglés: {random.choice(['Intermedio-Avanzado', 'Avanzado', 'Bilingüe'])}.

**Beneficios:**
- {'. '.join(random.sample(beneficios, k=random.randint(4, 6)))}
"""
    return desc

# --- Creación del Archivo CSV ---

def generar_csv(numero_de_filas):
    """Genera el archivo CSV con la cantidad de datos especificada."""
    nombre_archivo = 'candidatos_y_puestos.csv'
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        # Escribir la cabecera
        writer.writerow(['CV del Candidato', 'Descripción del Puesto'])

        # Generar y escribir cada fila
        for i in range(numero_de_filas):
            cv_candidato = generar_cv()
            descripcion_puesto = generar_descripcion_puesto()
            writer.writerow([cv_candidato, descripcion_puesto])
            # Imprimir progreso en la consola
            if (i + 1) % 1000 == 0:
                print(f"Generando... {i + 1}/{numero_de_filas} filas completadas.")

    print(f"\n¡Proceso completado! Se ha generado el archivo '{nombre_archivo}' con {numero_de_filas} filas.")

# --- Ejecutar el generador ---
if __name__ == '__main__':
    # Define aquí el número de filas que deseas generar
    NUMERO_DE_FILAS_A_GENERAR = 200000
    generar_csv(NUMERO_DE_FILAS_A_GENERAR)
    