"""
QUICK START: USAR EL MODELO COMO AGENTE
Referencia rápida para implementar agentes basados en tu modelo
"""

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║             ⚡ QUICK START: IMPLEMENTAR UN AGENTE EN 5 MIN ⚡             ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝


🎯 OPCIÓN 1: AGENTE SIMPLE (RECOMENDADO PARA EMPEZAR)
════════════════════════════════════════════════════════════════════════════

Archivo: agents_simple.py

Uso:
────

from agents_simple import SimpleRecruitmentAgent

agent = SimpleRecruitmentAgent("./model")

# Test búsqueda
print(agent.process_query("Busca un desarrollador Python senior"))

# Test matching
print(agent.process_query("Match: 'Senior Developer' con 'Python Engineer'"))

# Test clustering
print(agent.process_query("Agrupa candidatos en 3 grupos"))

✅ VENTAJAS:
  • Rápido de implementar
  • No requiere API keys
  • Funciona offline
  • Perfecto para MVP

❌ LIMITACIONES:
  • Solo reglas simples
  • No entiende lenguaje natural flexible
  • Difícil de escalar


────────────────────────────────────────────────────────────────────────────

🎯 OPCIÓN 2: AGENTE AVANZADO CON FUNCIONES
════════════════════════════════════════════════════════════════════════════

Archivo: agents_advanced.py

Uso:
────

from agents_advanced import AdvancedRecruitmentAgent

agent = AdvancedRecruitmentAgent("./model")

# Búsqueda
results = agent.search_candidates("Senior Python Developer", top_k=5)

# Matching detallado
match = agent.calculate_candidate_job_match("C001", "J001")
print(f"Score: {match['overall_score']:.1%}")
print(f"Recomendación: {match['recommendation']}")

# Recomendaciones para candidato
jobs = agent.get_job_recommendations_for_candidate("C001", top_k=3)

# Top candidatos para posición
candidates = agent.get_top_candidates_for_job("J001", top_k=5)

✅ VENTAJAS:
  • Funciones específicas para cada caso
  • Matching detallado con múltiples scores
  • Gestión de estado/contexto
  • Historial de conversación
  • Memory para contexto

✅ CASOS DE USO:
  • Screening automático
  • Recomendaciones personalizadas
  • Análisis de matching
  • Batch processing


────────────────────────────────────────────────────────────────────────────

🎯 OPCIÓN 3: API REST (PARA PRODUCCIÓN)
════════════════════════════════════════════════════════════════════════════

Archivo: agent_api.py

Instalación:
────────────

pip install fastapi uvicorn pydantic

Ejecutar:
─────────

uvicorn agent_api:app --reload --port 8000

Luego acceder a:
  • Swagger: http://localhost:8000/docs
  • ReDoc: http://localhost:8000/redoc

Ejemplos de uso:
────────────────

# Health check
curl http://localhost:8000/health

# Listar candidatos
curl http://localhost:8000/candidates

# Buscar
curl -X POST http://localhost:8000/candidates/search \\
  -H "Content-Type: application/json" \\
  -d '{"query": "Python Developer", "top_k": 5}'

# Matching
curl -X POST http://localhost:8000/match \\
  -H "Content-Type: application/json" \\
  -d '{"candidate_id": "C001", "job_id": "J001"}'

# Query conversacional
curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Busca desarrolladores Python"}'

✅ VENTAJAS:
  • Exposición como servicio
  • Escalable
  • Documentación automática (Swagger)
  • Fácil de integrar con otros sistemas
  • Auth y rate limiting posible
  • Deployment en contenedores

✅ ENDPOINTS:
  GET  /health                    - Health check
  GET  /info                      - Info del agente
  GET  /candidates                - Listar candidatos
  GET  /candidates/{id}           - Detalles candidato
  POST /candidates/search         - Buscar candidatos
  GET  /jobs                      - Listar posiciones
  POST /match                     - Calcular matching
  GET  /jobs/{id}/top-candidates  - Top candidatos
  POST /query                     - Query conversacional
  POST /batch/screen-cv           - Screening automático


────────────────────────────────────────────────────────────────────────────

🎯 OPCIÓN 4: INTEGRACIÓN CON LANGCHAIN + LLM
════════════════════════════════════════════════════════════════════════════

Para máxima flexibilidad con procesamiento de lenguaje natural:

pip install langchain openai

Código:
───────

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from agents_advanced import AdvancedRecruitmentAgent

# Crear agente
model_agent = AdvancedRecruitmentAgent("./model")

# Definir herramientas
tools = [
    Tool(
        name="Search Candidates",
        func=model_agent.search_candidates,
        description="Search for candidates based on a query"
    ),
    Tool(
        name="Match Candidate Job",
        func=model_agent.calculate_candidate_job_match,
        description="Calculate match between candidate and job"
    ),
    Tool(
        name="Recommend Jobs",
        func=model_agent.get_job_recommendations_for_candidate,
        description="Get job recommendations for a candidate"
    ),
]

# Crear agente LLM
llm = OpenAI(temperature=0.7, api_key="tu-api-key")
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Usar
response = agent.run(
    "Find top candidates for a senior python developer position"
)

✅ VENTAJAS:
  • Entiende lenguaje natural complejo
  • Razonamiento multi-paso
  • Muy flexible y potente

⚠️ CONSIDERACIONES:
  • Costo: ~$0.01-0.05 por query (OpenAI)
  • Latencia: 1-5 segundos
  • Requiere API key


════════════════════════════════════════════════════════════════════════════

📊 COMPARACIÓN DE OPCIONES
════════════════════════════════════════════════════════════════════════════

                SIMPLE    ADVANCED    API       LANGCHAIN
────────────────────────────────────────────────────────────
Complejidad     ⭐       ⭐⭐⭐       ⭐⭐      ⭐⭐⭐⭐
Velocidad       🟢⚡     🟡         🟡        🔴
Costo           🟢       🟢          🟢        🔴$ (LLM)
Escalabilidad   🔴       🟡         🟢        🟢
Flexibilidad    🔴       🟡         🟡        🟢⭐
NL entendim.    🔴       🟡         🟡        🟢⭐
Fácil uso       🟢       🟡         🟢        🔴
Producción      🔴       🟡         🟢        🟢

RECOMENDACIÓN:
  • MVP: SimpleRecruitmentAgent (agents_simple.py)
  • Production: API REST (agent_api.py) + LangChain (optional)


════════════════════════════════════════════════════════════════════════════

🚀 EJEMPLOS DE IMPLEMENTACIÓN POR CASO DE USO
════════════════════════════════════════════════════════════════════════════

CASO 1: CHATBOT DE RECRUITMENT
───────────────────────────────

while True:
    user_input = input("\\nTú: ")
    if user_input.lower() == "salir":
        break
    
    response = agent.process_query(user_input)
    print(f"Agente: {response}")

Usuarios pueden:
  ✅ Buscar candidatos naturalmente
  ✅ Hacer preguntas sobre matches
  ✅ Solicitar recomendaciones
  ✅ Mantener conversación


CASO 2: SCREENING AUTOMÁTICO
──────────────────────────────

import pandas as pd

# Cargar CVs nuevos
new_cvs = pd.read_csv("new_cvs.csv")

for idx, row in new_cvs.iterrows():
    profile = row['cv_text']
    
    # Usar API
    response = requests.post(
        "http://localhost:8000/batch/screen-cv",
        json={"profile": profile}
    )
    
    result = response.json()
    best_fit = result['best_fit']
    
    print(f"CV {idx}: Mejor posición = {best_fit['job_title']}")


CASO 3: ANÁLISIS DE TALENTO
──────────────────────────────

# Clustering de candidatos
clusters = agent.model.cluster(
    [c["profile"] for c in agent.candidates_db],
    n_clusters=5
)

# Analizar por cluster
for cluster_id, profiles in clusters.items():
    print(f"\\nCluster {cluster_id}:")
    print(f"  Tamaño: {len(profiles)}")
    # Análisis de skills del cluster...


CASO 4: MATCHING A ESCALA
────────────────────────────

# Matchear todos los candidatos a una posición
results = []
for candidate in agent.candidates_db:
    match = agent.calculate_candidate_job_match(
        candidate["id"],
        "J001"
    )
    results.append(match)

# Ordenar por score
results.sort(key=lambda x: x["overall_score"], reverse=True)

# Top 5
for i, match in enumerate(results[:5], 1):
    print(f"{i}. {match['candidate']['name']}: {match['overall_score']:.1%}")


════════════════════════════════════════════════════════════════════════════

📈 ARQUITECTURA RECOMENDADA PARA PRODUCCIÓN
════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────┐
│      Frontend (Web/Mobile)              │
│   - React/Vue                           │
│   - Interfaz de usuario                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      API REST (FastAPI)                 │
│   - agent_api.py                        │
│   - Endpoints principales               │
│   - Rate limiting, Auth                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Agent Layer                        │
│   - AdvancedRecruitmentAgent            │
│   - State management                    │
│   - Tool orchestration                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Model Layer                        │
│   - Tu modelo (embeddings)              │
│   - Búsqueda, matching, clustering      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Data Layer                         │
│   - PostgreSQL (CVs, jobs)              │
│   - Redis cache (embeddings)            │
│   - Elasticsearch (búsqueda full-text)  │
└─────────────────────────────────────────┘


════════════════════════════════════════════════════════════════════════════

📁 ARCHIVOS DEL PROYECTO
════════════════════════════════════════════════════════════════════════════

loader.py                  - Cargador del modelo (base)
agents_simple.py           - Agente simple con reglas
agents_advanced.py         - Agente avanzado con funciones
agent_api.py              - API REST con FastAPI
AGENT_GUIDE.md            - Guía completa de agentes (este archivo)
QUICK_AGENT_REFERENCE.py  - Quick start (este archivo)

Ejemplos de datos:
  - candidates_db: Lista de candidatos
  - jobs_db: Lista de posiciones
  - conversation_history: Historial


════════════════════════════════════════════════════════════════════════════

💡 TIPS Y MEJORES PRÁCTICAS
════════════════════════════════════════════════════════════════════════════

1. CACHING DE EMBEDDINGS
   ✅ Pre-calcular embeddings de CVs/jobs
   ✅ Guardar en Redis
   ✅ Reutilizar para búsquedas frecuentes
   ✅ Reduce latencia 10x

2. BATCH PROCESSING
   ✅ Para procesar muchos CVs
   ✅ Usar endpoints /batch/*
   ✅ Guardar resultados en DB

3. MONITOREO
   ✅ Log de queries
   ✅ Métricas de matching
   ✅ Feedback de usuarios
   ✅ Reentrenamiento periódico

4. SEGURIDAD
   ✅ Autenticación en API
   ✅ Rate limiting
   ✅ Validación de inputs
   ✅ HTTPS en producción

5. PERFORMANCE
   ✅ Usar GPU si disponible
   ✅ Batch inference
   ✅ Load balancing
   ✅ Monitoreo de latencia


════════════════════════════════════════════════════════════════════════════

🎓 PRÓXIMOS PASOS
════════════════════════════════════════════════════════════════════════════

1. ✅ Empezar con agents_simple.py
   → Probar funcionalidad básica
   → Entender el flujo

2. ✅ Integrar agents_advanced.py
   → Funciones más complejas
   → Mejor scoring

3. ✅ Crear API REST (agent_api.py)
   → Exposer como servicio
   → Testing de endpoints

4. ✅ Agregar LangChain (opcional)
   → Para mejor NL understanding
   → Más casos de uso

5. ✅ Deploying a producción
   → Docker
   → Kubernetes
   → Monitoreo


════════════════════════════════════════════════════════════════════════════

❓ PREGUNTAS FRECUENTES
════════════════════════════════════════════════════════════════════════════

P: ¿Cuánta latencia tiene el agente?
R: Simple: 50ms, Advanced: 100-200ms, API: +network, LLM: 1-5s

P: ¿Puedo usarlo offline?
R: Sí, con SimpleRecruitmentAgent o AdvancedRecruitmentAgent localmente

P: ¿Soporta múltiples usuarios concurrentes?
R: Sí con API REST + load balancing

P: ¿Necesito GPU?
R: No, CPU funciona bien. GPU da 10x speedup opcional.

P: ¿Cómo manejo errores?
R: Try-catch en funciones, error handlers en API

P: ¿Cómo actualizó el modelo?
R: Reemplazar archivo model.safetensors, reiniciar servicio


════════════════════════════════════════════════════════════════════════════
""")
