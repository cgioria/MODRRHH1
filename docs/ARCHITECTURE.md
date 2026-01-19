# 🏗️ ARQUITECTURA DEL PROYECTO

Descripción técnica de la estructura y componentes del sistema.

## 📊 Visión General

```
┌─────────────────────────────────────────────────────┐
│         CAPA DE PRESENTACIÓN                        │
│  (Usuarios, Navegadores, Clientes)                 │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│         CAPA DE API (FastAPI)                       │
│  • REST Endpoints                                   │
│  • WebSocket (opcional)                             │
│  • Validación Pydantic                              │
│  • Rate Limiting                                    │
│  • Authentication                                   │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│      CAPA DE AGENTES (Recruitment)                  │
│  • SimpleRecruitmentAgent                           │
│  • AdvancedRecruitmentAgent                         │
│  • Tool System                                      │
│  • Memory/State Management                          │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│      CAPA DE MODELO (Sentence Transformers)         │
│  • paraphrase-multilingual-mpnet-base-v2            │
│  • 768 dimensiones                                  │
│  • 9 idiomas soportados                             │
│  • GPU/CPU support                                  │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│      CAPA DE DATOS                                  │
│  • Database (PostgreSQL)                            │
│  • Cache (Redis)                                    │
│  • Embeddings Storage                               │
│  • Audit Trail                                      │
└─────────────────────────────────────────────────────┘
```

## 🗂️ Estructura de Directorios

```
modelo_entrenado_multiloss_portable/
│
├── 📚 CORE (Núcleo)
│   ├── model/                        # Modelo entrenado (768 dims)
│   ├── loader.py                     # Cargador universal
│   └── MODEL_INFO.json               # Metadata
│
├── 🤖 AGENTES
│   ├── agents_simple.py              # MVP - Reglas simples
│   ├── agents_advanced.py            # Producción - Estado completo
│   ├── agent_api.py                  # FastAPI - REST API
│   ├── docs/                         # Documentación
│   │   ├── GUIDE.md
│   │   ├── SUMMARY.md
│   │   └── REFERENCE.py
│   ├── tests/                        # Suite de pruebas
│   └── README.md
│
├── 📊 EVALUACIÓN
│   ├── evaluate_model.py             # Script de evaluación
│   ├── EVALUATION_REPORT.txt         # Reporte
│   ├── evaluation_results.json       # Resultados
│   └── README.md
│
├── 💼 EJEMPLOS
│   ├── python/                       # Uso directo en Python
│   ├── api/                          # Uso vía API
│   ├── integrations/                 # Django, Flask, etc.
│   └── README.md
│
├── 🚀 DEPLOYMENT
│   ├── Dockerfile                    # Containerización
│   ├── docker-compose.yml            # Orquestación local
│   ├── nginx.conf                    # Reverse proxy
│   ├── kubernetes/                   # Manifiestos K8s
│   └── README.md
│
├── 📖 DOCUMENTACIÓN
│   ├── README.md                     # Inicio
│   ├── QUICKSTART.md                 # 5 minutos
│   ├── ARCHITECTURE.md               # Este archivo
│   ├── INDEX.md                      # Índice
│   └── docs/                         # Archivos adicionales
│
└── ⚙️ CONFIGURACIÓN
    ├── requirements.txt              # Dependencias Python
    ├── .env.example                  # Variables de entorno
    ├── config.yaml                   # Configuración
    └── api_wrapper.py                # API standalone
```

## 🧠 Componentes Principales

### 1. Capa de Modelo

**Archivo:** `model/` + `loader.py`

**Responsabilidades:**
- Cargar modelo Sentence Transformers
- Generar embeddings (768 dimensiones)
- Cálcular similitud entre textos
- Búsqueda semántica
- Clustering de textos

**Modelos soportados:**
- `paraphrase-multilingual-mpnet-base-v2` (default)
- Customizable a otros modelos

**Performance:**
- CPU: 22 textos/segundo
- GPU: 200+ textos/segundo
- Memory: ~1GB

### 2. Capa de Agentes

#### 2a. SimpleRecruitmentAgent

**Archivo:** `agent/agents_simple.py`

**Características:**
- Regex-based pattern matching
- 5 intents: search, match, similarity, cluster, help
- Sin estado (stateless)
- Bajo overhead

**Métodos clave:**
```python
process_query(query: str) -> str
_handle_search(query: str) -> List[Dict]
_handle_matching(text1: str, text2: str) -> Dict
_handle_clustering(n_clusters: int) -> Dict
```

**Casos de uso:**
- MVP/Prototipo rápido
- Demo simple
- Testing básico

#### 2b. AdvancedRecruitmentAgent

**Archivo:** `agent/agents_advanced.py`

**Características:**
- Tool-based architecture
- 5 herramientas: search, matching, recommendations, analysis
- State management + Memory
- Multi-dimensional scoring

**Métodos clave:**
```python
search_candidates(query: str) -> List[Dict]
calculate_candidate_job_match(candidate_id, job_id) -> Dict
get_top_candidates_for_job(job_id) -> List[Dict]
get_job_recommendations_for_candidate(candidate_id) -> List[Dict]
```

**Casos de uso:**
- Backend de aplicación
- Análisis profundo
- Recomendaciones personalizadas

#### 2c. Agent API (FastAPI)

**Archivo:** `agent/agent_api.py`

**Características:**
- 15+ endpoints REST
- Swagger/OpenAPI documentation
- Pydantic validation
- CORS support
- Rate limiting ready

**Endpoints principales:**
```
GET    /health                     # Health check
GET    /info                       # Info del agente
POST   /candidates/search          # Buscar candidatos
POST   /match                      # Matching job-candidate
GET    /candidates/{id}/jobs       # Recomendaciones
POST   /batch/match-all            # Batch processing
```

**Casos de uso:**
- Apps web
- Múltiples usuarios
- Escalabilidad

### 3. Capa de Evaluación

**Archivos:** `evaluation/`

**6 tipos de métricas:**
1. Velocidad de inferencia
2. Similitud (mean, std, accuracy)
3. Búsqueda (MRR, NDCG, Precision@k)
4. Clustering (cohesión)
5. Distribución de embeddings
6. Performance multilingüe

### 4. Capa de Datos (Futura)

**Será implementado:**
- PostgreSQL para candidatos/jobs
- Redis para cache de embeddings
- Elasticsearch para full-text search

**Estructura actual:** In-memory dictionaries (demo)

## 🔄 Flujos de Datos

### Flujo 1: Búsqueda de Candidatos

```
User Query
    ↓
Agent.process_query()
    ↓
Pattern Matching (intent)
    ↓
_handle_search()
    ↓
Model.search()
    ↓
model.encode(query) → embeddings
    ↓
Similitud coseno con candidatos
    ↓
Ranking por similitud
    ↓
Formatted Response
    ↓
User
```

### Flujo 2: API Request

```
HTTP Request (POST /match)
    ↓
FastAPI endpoint
    ↓
Pydantic validation
    ↓
Agent.calculate_match()
    ↓
Model.similarity()
    ↓
JSON Response
    ↓
Client
```

### Flujo 3: Batch Processing

```
Bulk Upload (POST /batch/match-all)
    ↓
Queue Processing
    ↓
Parallel Encoding
    ↓
Batch Similarity Calculation
    ↓
Store Results
    ↓
Return Summary
```

## 💾 Modelos de Datos

### Candidate

```python
{
    "id": "c001",
    "name": "Alice",
    "profile": "Senior Python Developer with 10 years experience",
    "skills": ["Python", "Django", "PostgreSQL"],
    "experience_years": 10,
    "embedding": [768-dim vector],
    "last_updated": "2024-01-16"
}
```

### Job

```python
{
    "id": "j001",
    "title": "Senior Backend Engineer",
    "description": "We need a Python expert...",
    "required_skills": ["Python", "APIs"],
    "embedding": [768-dim vector],
    "posted_date": "2024-01-01"
}
```

### Match Result

```python
{
    "candidate_id": "c001",
    "job_id": "j001",
    "overall_score": 0.88,
    "profile_similarity": 0.90,
    "skills_match": 0.85,
    "experience_match": 0.95,
    "recommendation": "Strong match"
}
```

## ⚙️ Opciones de Configuración

### Environment Variables

```bash
# Model
MODEL_PATH=./model
DEVICE=cpu                   # cpu|cuda
MODEL_BATCH_SIZE=32

# API
PORT=8000
WORKERS=4
THREADS_PER_WORKER=2

# Logging
LOG_LEVEL=info               # debug|info|warning|error
LOG_FILE=./logs/api.log

# Performance
CACHE_EMBEDDINGS=true
CACHE_TTL=3600               # segundos

# Security
RATE_LIMIT=1000              # requests per minute
MAX_TEXT_LENGTH=10000        # characters
REQUIRE_AUTH=false
```

## 🔐 Consideraciones de Seguridad

1. **Input Validation**
   - Longitud máxima de texto
   - Rate limiting
   - SQL injection prevention (futura DB)

2. **Authentication**
   - API keys (opcional)
   - JWT tokens (futuro)

3. **Data Privacy**
   - No guardar embeddings personales
   - Anonimización de logs
   - GDPR compliance (futuro)

4. **Resource Limits**
   - Timeout en requests
   - Memory limits en container
   - CPU throttling

## 📈 Escalabilidad

### Vertical Scaling (Single Machine)

```
CPU: 1 → 4 cores
RAM: 4GB → 16GB
GPU: CPU → T4/V100
```

**Mejora esperada:** 2-4x throughput

### Horizontal Scaling (Multiple Machines)

```
Load Balancer
    ↓
├─ API Instance 1
├─ API Instance 2
└─ API Instance 3
    ↓
Shared Database
Shared Cache (Redis)
```

**Mejora esperada:** N x throughput (lineal)

### Optimization Strategies

1. **Embedding Cache**
   - Redis cache de embeddings frecuentes
   - TTL configurable

2. **Batch Processing**
   - Procesar múltiples queries simultaneamente
   - Utilizar GPU batch size optimizado

3. **Model Quantization**
   - Reducir tamaño del modelo
   - Compilación ONNX (futuro)

4. **Approximate Similarity**
   - Usar indices ANN (FAISS)
   - Trade-off accuracy vs speed (futuro)

## 🧪 Testing

### Niveles de Testing

```
Unit Tests
├─ Test loader.py
├─ Test similarity()
└─ Test encoding()

Integration Tests
├─ Test Agent + Model
├─ Test API endpoints
└─ Test with sample data

Performance Tests
├─ Throughput benchmarks
├─ Latency percentiles
└─ Memory profiling

End-to-End Tests
├─ Full workflow
├─ Real data
└─ Production-like setup
```

## 📚 Dependencias

### Core
- `sentence-transformers>=2.2.0` - Modelo
- `numpy>=1.21.0` - Arrays
- `torch>=2.0.0` - ML backend
- `scikit-learn>=1.0.0` - Clustering

### API
- `fastapi>=0.95.0` - Web framework
- `uvicorn>=0.21.0` - ASGI server
- `pydantic>=2.0.0` - Validation

### Data (Futura)
- `psycopg2>=2.9.0` - PostgreSQL
- `redis>=4.0.0` - Cache
- `elasticsearch>=8.0.0` - Search

### Deployment
- `docker>=20.10` - Containerization
- `kubernetes>=1.24` - Orchestration

---

**Versión:** 1.0
**Última actualización:** Enero 2026
