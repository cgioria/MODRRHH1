# 📑 ÍNDICE COMPLETO DEL PROYECTO

Mapa de navegación del proyecto completo.

## 🎯 Punto de Entrada

- **README.md** - Inicio del proyecto (COMIENZA AQUÍ)
- **QUICKSTART.md** - 5 minutos para empezar
- **ARCHITECTURE.md** - Descripción técnica completa

---

## 📚 DOCUMENTACIÓN

### Principal

| Archivo | Descripción | Tiempo |
|---------|-------------|--------|
| README.md | Introducción y setup | 5 min |
| QUICKSTART.md | 5 opciones de uso | 5 min |
| ARCHITECTURE.md | Descripción técnica | 15 min |
| INDEX.md | Este archivo | 5 min |

### Complementaria

| Archivo | Ubicación | Tema |
|---------|-----------|------|
| PLAN_REORGANIZACION.md | docs/ | Cómo se reorganizó el proyecto |
| REORGANIZACION.md | docs/ | Cambios realizados |
| DEPLOYMENT.md | docs/ | Deployment legacy |
| INTEGRACION.md | docs/ | Integración legacy |
| RESUMEN_TRABAJO_COMPLETADO.md | docs/ | Historial del proyecto |

---

## 🧠 CORE (Modelo)

### model/

```
model/
├── model.safetensors             # Pesos del modelo (168 MB)
├── config.json                   # Configuración Sentence Transformers
├── config_sentence_transformers.json
├── tokenizer.json                # Tokenizer
├── tokenizer_config.json         # Config del tokenizer
├── special_tokens_map.json       # Tokens especiales
├── sentencepiece.bpe.model       # BPE model
├── modules.json                  # Módulos
├── 1_Pooling/config.json         # Pooling config
├── training_metadata.json        # Metadata de entrenamiento
├── README.md                     # Información del modelo
└── eval/                         # Datos de evaluación
```

### loader.py

```python
from loader import load_model, ModeloPortable

# Uso
model = load_model('./model')
embeddings = model.encode(['text1', 'text2'])
similarity = model.similarity('text1', 'text2')
results = model.search('query', candidates, top_k=5)
clusters = model.cluster(texts, n_clusters=3)
```

### MODEL_INFO.json

Metadata del modelo:
- Nombre: paraphrase-multilingual-mpnet-base-v2
- Dimensiones: 768
- Idiomas: 9
- Especialización: Recruitment

---

## 🤖 AGENTES

### agent/

```
agent/
├── agents_simple.py              # MVP (350 líneas)
├── agents_advanced.py            # Producción (577 líneas)
├── agent_api.py                  # FastAPI (502 líneas)
├── README.md                     # Guía de agentes
├── docs/
│   ├── GUIDE.md                  # Guía completa (2000+ líneas)
│   ├── SUMMARY.md                # Resumen ejecutivo
│   └── REFERENCE.py              # Quick reference
└── tests/
    └── (test files)              # Suite de pruebas
```

### Uso Rápido

**Opción 1: Simple Agent**
```bash
python agent/agents_simple.py
```

**Opción 2: Advanced Agent**
```bash
python agent/agents_advanced.py
```

**Opción 3: API REST**
```bash
uvicorn agent.agent_api:app --reload --port 8000
# Acceder a: http://localhost:8000/docs
```

### Características por Agente

| Característica | Simple | Advanced | API |
|---------------|--------|----------|-----|
| MVP Ready | ✅ | ✅ | ✅ |
| Producción | ⭐ | ✅✅ | ✅✅✅ |
| State | ❌ | ✅ | ✅ |
| Memory | ❌ | ✅ | ✅ |
| Tools | 5 | 5+ | 15+ |
| Multiuser | ❌ | ⭐ | ✅ |
| Escalable | ❌ | ⭐ | ✅✅ |

---

## 📊 EVALUACIÓN

### evaluation/

```
evaluation/
├── evaluate_model.py             # Script principal (340 líneas)
├── EVALUATION_REPORT.txt         # Reporte formateado
├── evaluation_results.json       # Resultados en JSON
├── HOW_TO_MEASURE_PERFORMANCE.py # Guía (200+ líneas)
├── QUICK_PERFORMANCE_TEST.py     # Test rápido (100+ líneas)
└── README.md                     # Guía de evaluación
```

### Métricas Implementadas

1. **Velocidad de Inferencia**
   - 100 textos: 4.49 segundos
   - 22 textos/segundo en CPU
   - 44.85ms por texto

2. **Similitud**
   - Media: 0.7702
   - Rango: [0.4043, 0.9985]
   - Precisión: 44.4%

3. **Búsqueda**
   - MRR: 1.0000 ✅✅✅ EXCELENTE
   - NDCG: 0.9931 ✅✅✅ EXCELENTE
   - Precision@5: 1.0000 ✅

4. **Clustering**
   - 9 textos en 3 clusters
   - Cohesión: 0.5427

5. **Multilingüe**
   - English: 0.8649
   - Spanish: 0.9482
   - Portuguese: 0.9201
   - German: 0.9536
   - Promedio: 0.91

### Uso

```bash
# Full evaluation
cd evaluation
python evaluate_model.py

# Quick test
python QUICK_PERFORMANCE_TEST.py

# Ver resultados
cat EVALUATION_REPORT.txt
cat evaluation_results.json
```

---

## 💼 EJEMPLOS

### examples/

```
examples/
├── python/
│   ├── example_python.py         # Uso básico en Python
│   ├── basic_usage.py            # (futuro)
│   ├── similarity_search.py       # (futuro)
│   └── clustering.py             # (futuro)
├── api/
│   ├── example_api_client.py      # Cliente Python para API
│   └── requests.sh               # (futuro)
├── integrations/
│   ├── example_django.py          # Django integration
│   ├── example_flask.py           # Flask integration
│   └── (más frameworks)          # (futuro)
└── README.md                     # Guía de ejemplos
```

### Frameworks Soportados

- ✅ Python nativo
- ✅ Django
- ✅ Flask
- ⭐ FastAPI (ver agent/agent_api.py)
- ⭐ REST API (agent/agent_api.py)

---

## 🚀 DEPLOYMENT

### deployment/

```
deployment/
├── Dockerfile                    # Imagen Docker
├── docker-compose.yml            # Orquestación local
├── nginx.conf                    # Reverse proxy Nginx
├── kubernetes/
│   └── deployment.yaml           # Manifesto K8s
└── README.md                     # Guía de deployment
```

### Opciones de Despliegue

| Opción | Complejidad | Tiempo | Escalabilidad |
|--------|-------------|--------|---------------|
| Local Python | ⭐ | 5 min | ❌ |
| Docker | ⭐⭐ | 10 min | ⭐ |
| Docker Compose | ⭐⭐ | 10 min | ⭐⭐ |
| Kubernetes | ⭐⭐⭐ | 30 min | ⭐⭐⭐ |

### Quick Commands

```bash
# Docker
docker build -t recruitment-model .
docker run -p 8000:8000 recruitment-model

# Docker Compose
docker-compose up -d

# Kubernetes
kubectl apply -f kubernetes/deployment.yaml
```

---

## ⚙️ CONFIGURACIÓN

### Raíz

```
├── requirements.txt              # Dependencias Python
├── .env.example                  # Template de variables
├── config.yaml                   # Config general (futuro)
└── api_wrapper.py                # API standalone
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Variables de Entorno

```bash
cp .env.example .env
# Editar .env con tus valores
source .env  # Linux/Mac
set -a; source .env; set +a  # Bash
$env:file = Get-Content .env; Invoke-Expression $env:file  # PowerShell
```

---

## 📂 ESTRUCTURA RESUMEN

```
modelo_entrenado_multiloss_portable/ (raíz)
├── 📖 README.md                  ← COMIENZA AQUÍ
├── ⚡ QUICKSTART.md               ← 5 MINUTOS
├── 🏗️ docs/
│   ├── ARCHITECTURE.md           ← TÉCNICO
│   ├── INDEX.md                  ← ESTE ARCHIVO
│   └── (documentación adicional)
├── 🧠 model/                      ← MODELO ENTRENADO
├── 🤖 agent/                      ← AGENTES (MVP, Advanced, API)
├── 📊 evaluation/                 ← EVALUACIÓN & MÉTRICAS
├── 💼 examples/                   ← EJEMPLOS DE USO
├── 🚀 deployment/                 ← DOCKER, K8s
├── ⚙️ loader.py                   ← CARGADOR UNIVERSAL
└── 📋 requirements.txt            ← DEPENDENCIAS
```

---

## 🎓 Rutas de Aprendizaje

### Para Principiantes (30 min)
1. Leer README.md
2. Ejecutar QUICKSTART.md opción 1
3. Ver agent/agents_simple.py funcionando
4. Explorar examples/python/

### Para Desarrolladores (2 horas)
1. Leer QUICKSTART.md (todas las opciones)
2. Ejecutar evaluation/evaluate_model.py
3. Revisar agent_api.py y probarlo
4. Estudiar docs/ARCHITECTURE.md

### Para DevOps/SRE (3 horas)
1. Leer deployment/README.md
2. Build y run Docker
3. Ejecutar docker-compose
4. Deployar en Kubernetes

### Para Científicos de Datos (4 horas)
1. Estudiar model/training_metadata.json
2. Ejecutar evaluation/ completo
3. Analizar evaluation_results.json
4. Revisar agent/ para entender el modelo

---

## 🔗 Referencias Cruzadas

### Si quieres...

| Objetivo | Ir a | Tiempo |
|----------|------|--------|
| Empezar en 5 min | QUICKSTART.md | 5 min |
| Entender arquitectura | ARCHITECTURE.md | 15 min |
| Usar el modelo | loader.py + examples/ | 10 min |
| Evaluar rendimiento | evaluation/evaluate_model.py | 5 min |
| Usar como API | agent/agent_api.py | 15 min |
| Deployar | deployment/README.md | 30 min |
| Integrar en app | examples/integrations/ | 20 min |
| Entender agentes | agent/docs/ | 30 min |
| Contribute | CONTRIBUTING.md (futuro) | - |

---

## 📞 Soporte

### Problemas Comunes

1. **"No se encuentra el modelo"**
   - Verificar: `ls -la model/model.safetensors`
   - Solución: Descargar modelo en `model/`

2. **"Out of Memory"**
   - Cambiar device: `loader.py` → device="cpu"
   - O reducir batch size en config

3. **"Puerto 8000 en uso"**
   - Cambiar puerto: `uvicorn ... --port 9000`
   - O detener otro proceso: `lsof -i :8000`

4. **"Import error"**
   - Instalar deps: `pip install -r requirements.txt`
   - Activar venv: `. .venv/bin/activate`

---

## 🔄 Versioning

- **Proyecto**: v1.0 (2026-01-16)
- **Modelo**: paraphrase-multilingual-mpnet-base-v2
- **Framework**: Sentence Transformers 2.2+
- **Python**: 3.8+

---

**Última actualización:** 2026-01-16
**Mantenedor:** Sistema de Recruitment
