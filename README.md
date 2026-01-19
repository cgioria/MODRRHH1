# 🎯 Recruitment Model - Sistema de Semantic Search & Agentes

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Torch](https://img.shields.io/badge/Torch-2.0+-red.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> **Sistema integral de búsqueda semántica y agentes inteligentes para recruitment**

## 🚀 Quick Start (5 minutos)

### Opción 1: Python Directo (Más Rápido)
```bash
pip install -r requirements.txt
python agent/agents_simple.py
```

### Opción 2: API REST
```bash
pip install fastapi uvicorn -r requirements.txt
uvicorn agent.agent_api:app --reload --port 8000
# Acceder a: http://localhost:8000/docs
```

### Opción 3: Docker
```bash
docker build -t recruitment-model deployment/
docker run -p 8000:8000 recruitment-model
```

---

## 📚 Documentación

| Documento | Descripción | Tiempo |
|-----------|-------------|--------|
| [QUICKSTART.md](QUICKSTART.md) | 5 opciones de setup | 5 min |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Descripción técnica | 15 min |
| [docs/INDEX.md](docs/INDEX.md) | Índice completo del proyecto | 10 min |
| [agent/README.md](agent/README.md) | Guía de agentes | 10 min |
| [evaluation/README.md](evaluation/README.md) | Evaluación de modelo | 5 min |
| [deployment/README.md](deployment/README.md) | Despliegue en producción | 10 min |

---

## 🎯 Características Principales

### ✨ Modelo Entrenado
- **Modelo**: paraphrase-multilingual-mpnet-base-v2
- **Dimensiones**: 768
- **Idiomas**: 9 (English, Spanish, Portuguese, French, German, Italian, Dutch, Romanian, Chinese)
- **Performance**: MRR 1.0, NDCG 0.9931 (excelente)
- **Velocidad**: 22 textos/seg en CPU, 200+ en GPU

### 🤖 Agentes Inteligentes
1. **SimpleRecruitmentAgent** - MVP rápido y simple
2. **AdvancedRecruitmentAgent** - Producción con state management
3. **REST API** - FastAPI con 15+ endpoints

### 📊 Evaluación Completa
- Velocidad de inferencia
- Similitud de textos
- Búsqueda y ranking (MRR, NDCG)
- Clustering de candidatos
- Análisis multilingüe

### 🚀 Deployment Listo
- Docker ✅
- Docker Compose ✅
- Kubernetes ✅
- Nginx Reverse Proxy ✅

---

## 📁 Estructura del Proyecto

```
modelo_entrenado_multiloss_portable/
│
├── 🧠 CORE
│   ├── model/                       # Modelo entrenado (768 dims)
│   ├── loader.py                    # Cargador universal
│   └── MODEL_INFO.json              # Metadata
│
├── 🤖 AGENTES
│   ├── agent/
│   │   ├── agents_simple.py         # MVP
│   │   ├── agents_advanced.py       # Producción
│   │   ├── agent_api.py             # REST API
│   │   └── docs/                    # Documentación
│   └── README.md
│
├── 📊 EVALUACIÓN
│   ├── evaluation/
│   │   ├── evaluate_model.py
│   │   ├── EVALUATION_REPORT.txt
│   │   └── evaluation_results.json
│   └── README.md
│
├── 💼 EJEMPLOS
│   ├── examples/
│   │   ├── python/
│   │   ├── api/
│   │   └── integrations/
│   └── README.md
│
├── 🚀 DEPLOYMENT
│   ├── deployment/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── nginx.conf
│   │   └── kubernetes/
│   └── README.md
│
└── 📖 DOCUMENTACIÓN
    ├── README.md                    # Este archivo
    ├── QUICKSTART.md                # Quick start
    ├── docs/ARCHITECTURE.md         # Arquitectura
    └── docs/INDEX.md                # Índice completo
```

---

## 🎯 Casos de Uso

### 1️⃣ Búsqueda de Candidatos
```python
from agent.agents_simple import SimpleRecruitmentAgent

agent = SimpleRecruitmentAgent()
result = agent.process_query("Busca desarrolladores Python senior")
print(result)
```

### 2️⃣ Matching Job-Candidate
```python
result = agent.process_query(
    "Match: 'Senior Backend Python Developer' con 'Python backend engineer'"
)
print(result)
# Score: 88.48% ✅
```

### 3️⃣ API REST
```python
import requests

response = requests.post(
    "http://localhost:8000/candidates/search",
    json={"query": "python developer", "top_k": 5}
)
results = response.json()
for candidate in results:
    print(f"{candidate['name']}: {candidate['score']:.2%}")
```

### 4️⃣ Clustering de Candidatos
```python
result = agent.process_query("Agrupa candidatos en 3 grupos")
# Agrupa automáticamente por especialidad
```

---

## 📊 Resultados de Evaluación

| Métrica | Resultado | Calidad |
|---------|-----------|---------|
| **MRR (Mean Reciprocal Rank)** | 1.0000 | ✅✅✅ EXCELENTE |
| **NDCG (Normalized DCG)** | 0.9931 | ✅✅✅ EXCELENTE |
| **Precision@5** | 1.0000 | ✅✅✅ PERFECTO |
| **Similitud promedio** | 0.7702 | ✅✅ MUY BUENO |
| **Velocidad** | 22 textos/seg | ✅ CPU |
| **Multilingüe** | 91% promedio | ✅✅ MUY BUENO |

### Rendimiento Multilingüe
- 🇬🇧 English: 0.8649
- 🇪🇸 Spanish: 0.9482
- 🇵🇹 Portuguese: 0.9201
- 🇩🇪 German: 0.9536
- 🇫🇷 French: 0.9279

---

## 🔧 Instalación

### Requisitos
- Python 3.8+
- pip o conda
- ~2GB de espacio en disco
- GPU (opcional, pero recomendada)

### Setup Rápido

```bash
# 1. Clonar/descargar proyecto
cd modelo_entrenado_multiloss_portable

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python -c "from loader import load_model; print('✅ OK')"
```

### Verificar GPU (Opcional)
```bash
python -c "import torch; print(f'GPU disponible: {torch.cuda.is_available()}')"
```

Si hay GPU, usar en loader.py:
```python
model = load_model('./model', device='cuda')
```

---

## 💡 Ejemplos de Código

### Ejemplo 1: Similitud Básica
```python
from loader import load_model

model = load_model('./model')

# Calcular similitud entre dos textos
sim = model.similarity("python developer", "java engineer")
print(f"Similitud: {sim:.4f}")  # 0.4523
```

### Ejemplo 2: Búsqueda Semántica
```python
candidatos = [
    "Senior Python Developer with 10 years experience",
    "Java Software Engineer",
    "Python backend engineer specializing in APIs",
]

resultados = model.search("python backend", candidatos, top_k=2)
# Retorna: [(3, 0.854), (1, 0.782)]  # índice, score
```

### Ejemplo 3: Clustering
```python
textos = [
    "Python developer",
    "Python engineer",
    "Java backend",
    "Frontend React",
]

clusters = model.cluster(textos, n_clusters=2)
# Agrupa automáticamente por similitud
```

### Ejemplo 4: API con FastAPI
```bash
# Terminal 1: Levantar API
uvicorn agent.agent_api:app --reload

# Terminal 2: Cliente
python -c "
import requests
r = requests.post('http://localhost:8000/query', 
    json={'text': 'Busca desarrolladores python'})
print(r.json())
"
```

---

## 🚀 Deployment

### Docker Local
```bash
cd deployment
docker build -t recruitment-model .
docker run -p 8000:8000 recruitment-model
```

### Docker Compose (Recomendado)
```bash
cd deployment
docker-compose up -d
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Kubernetes
```bash
cd deployment
kubectl apply -f kubernetes/deployment.yaml
kubectl port-forward svc/recruitment-api 8000:8000
```

### Cloud Deployment
```bash
# AWS ECS, GCP Cloud Run, Azure Container Instances
# Ver: deployment/README.md
```

---

## 🧪 Evaluación del Modelo

```bash
# Evaluación completa (2 minutos)
cd evaluation
python evaluate_model.py

# Test rápido (30 segundos)
python QUICK_PERFORMANCE_TEST.py

# Ver resultados
cat EVALUATION_REPORT.txt
```

---

## 📦 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/info` | Info del agente |
| POST | `/candidates/search` | Buscar candidatos |
| POST | `/match` | Matching job-candidate |
| GET | `/candidates/{id}/jobs` | Recomendaciones de jobs |
| POST | `/batch/match-all` | Batch matching |
| GET | `/docs` | Swagger UI |

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/candidates/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python developer", "top_k": 5}'
```

---

## 🔍 Troubleshooting

### "No se encuentra el modelo"
```bash
ls -la model/model.safetensors
# Si no existe, descargar desde Hugging Face
```

### "Out of Memory"
```bash
# Usar CPU en lugar de GPU
model = load_model('./model', device='cpu')

# O reducir batch size
```

### "Puerto 8000 en uso"
```bash
# Cambiar puerto
uvicorn agent.agent_api:app --port 9000
```

### "Import error"
```bash
pip install -r requirements.txt
python -m pip install --upgrade pip
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crear branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📈 Roadmap

- [ ] Integración con LangChain
- [ ] Soporte para OpenAI GPT
- [ ] Dashboard web
- [ ] Base de datos PostgreSQL
- [ ] Cache Redis
- [ ] Elasticsearch integration
- [ ] Monitoring y logging
- [ ] MLOps pipeline
- [ ] Fine-tuning con datos reales

---

## 📞 Soporte

### Documentación
- 📖 [QUICKSTART.md](QUICKSTART.md) - Inicio rápido
- 🏗️ [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Arquitectura
- 📑 [docs/INDEX.md](docs/INDEX.md) - Índice completo

### Ejemplos
- 💼 [examples/](examples/) - Múltiples ejemplos
- 🤖 [agent/](agent/) - Documentación de agentes
- 📊 [evaluation/](evaluation/) - Evaluación

### Issues
Para reportar bugs o pedir features: [crear issue]()

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## ✨ Agradecimientos

- Sentence Transformers (Hugging Face)
- FastAPI
- PyTorch
- scikit-learn

---

**Versión**: 1.0.0  
**Última actualización**: Enero 2026  
**Mantenedor**: Sistema de Recruitment

---

## 🎯 Próximos Pasos

1. **Ahora**: Leer [QUICKSTART.md](QUICKSTART.md)
2. **Después**: Ejecutar un agente
3. **Luego**: Revisar [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
4. **Finalmente**: Deployar en producción

**¡Vamos!** 🚀
