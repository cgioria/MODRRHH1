# 📚 EJEMPLOS DE USO

Este directorio contiene ejemplos prácticos de cómo usar el modelo entrenado en diferentes contextos.

## 📋 Ejemplos Disponibles

### 1. **example_python.py** - Uso Directo en Python ✨

Demuestra el uso del modelo como módulo Python directo.

```bash
cd examples
python example_python.py
```

**Incluye:**
- Generar embeddings
- Calcular similitud entre textos
- Búsqueda de candidatos
- Clustering de textos
- Procesamiento en batch
- Obtener información del modelo
- Patrón producción

**Tiempo estimado:** 2-3 minutos

**Requisitos previos:**
```bash
pip install torch sentence-transformers numpy scikit-learn
```

---

### 2. **example_api_client.py** - Cliente API REST 🌐

Demuestra cómo usar el modelo a través de la API REST.

**Paso 1: Iniciar el servidor API**

```bash
cd ..
python api_wrapper.py --port 8000
```

**Paso 2: En otra terminal, ejecutar el cliente**

```bash
cd examples
python example_api_client.py
```

**Incluye:**
- Health check
- Obtener información del modelo
- Generar embeddings
- Calcular similitud
- Búsqueda de candidatos
- Clustering
- Medición de rendimiento
- Acceso a documentación Swagger

**Tiempo estimado:** 2-3 minutos

**Requisitos previos:**
```bash
pip install requests
```

---

### 3. **example_flask.py** - Integración Flask 🔌

Demuestra cómo integrar el modelo en una aplicación Flask.

```bash
cd examples
python example_flask.py
```

**Endpoints disponibles:**

```
GET  /                           # Información de la API
GET  /health                     # Health check
GET  /api/candidates             # Listar todos
POST /api/search                 # Buscar candidatos
POST /api/similarity             # Similitud entre 2
GET  /api/cluster?n_clusters=3  # Agrupar
GET  /api/profile/<id>          # Perfil individual
```

**Ejemplo de uso:**

```bash
# Buscar
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python developer", "top_k": 3}'

# Similitud
curl -X POST http://localhost:5000/api/similarity \
  -H "Content-Type: application/json" \
  -d '{"candidate_id_1": 1, "candidate_id_2": 2}'

# Clustering
curl http://localhost:5000/api/cluster?n_clusters=3
```

**Incluye:**
- Clase Candidate para modelos
- Base de datos simulada
- 7 endpoints funcionales
- Manejo de errores
- CORS habilitado para integración frontend

**Tiempo estimado:** 2-3 minutos

**Requisitos previos:**
```bash
pip install flask flask-cors
```

---

### 4. **example_django.py** - Integración Django 🎯

Demuestra cómo integrar el modelo en Django.

**Incluye:**
- Configuración de settings.py
- Modelos Django (Candidate, JobPosting)
- Vistas con class-based views
- URLs routing
- Integraciones AJAX
- Template JavaScript

**Uso:**

En tu proyecto Django, copia el modelo:

```bash
cp -r modelo_entrenado_multiloss_portable/model /tu/django/project/models/
cp ../loader.py /tu/django/project/
```

En `settings.py`:

```python
from loader import load_model
MODELO = load_model("./models/model")
```

En tus vistas:

```python
from django.conf import settings

results = settings.MODELO.search(query, candidates)
```

**Requisitos previos:**
```bash
pip install django
```

---

## 🚀 Inicio Rápido

### Opción 1: Solo Python (más simple)

```bash
# 1. Copiar modelo
cp -r .. /tu/proyecto/modelo

# 2. Instalar dependencias
pip install -r ../requirements.txt

# 3. Usar en tu código
from loader import load_model
model = load_model("./modelo")
results = model.search("query", ["candidate1", "candidate2"])
```

### Opción 2: API REST (más flexible)

```bash
# Terminal 1: Iniciar servidor
python ../api_wrapper.py --port 8000

# Terminal 2: Usar el cliente
python example_api_client.py
```

### Opción 3: Framework Web

```bash
# Elegir tu framework preferido
python example_flask.py    # Flask
python example_django.py   # Django (adaptado para tu proyecto)
```

---

## 📊 Comparativa de Uso

| Aspecto | Python Directo | API REST | Flask | Django |
|---------|--------|---------|-------|--------|
| Complejidad | ⭐ Muy simple | ⭐⭐ Simple | ⭐⭐ Simple | ⭐⭐⭐ Media |
| Rendimiento | ⭐⭐⭐ Excelente | ⭐⭐ Bueno | ⭐⭐ Bueno | ⭐⭐ Bueno |
| Flexibilidad | ⭐⭐ Media | ⭐⭐⭐ Alta | ⭐⭐⭐ Alta | ⭐⭐⭐ Alta |
| Escalabilidad | ⭐⭐ Media | ⭐⭐⭐ Alta | ⭐⭐ Media | ⭐⭐⭐ Alta |
| Setup | <1 min | 5 min | 5 min | 10+ min |

---

## 🔧 Configuración Común

### Usar GPU

```python
from loader import load_model
model = load_model("./model", device="cuda")
```

### Cambiar puerto API

```bash
python ../api_wrapper.py --port 9000
```

### Recargar automáticamente (desarrollo)

```bash
python ../api_wrapper.py --reload
```

### Usar CPU explícitamente

```bash
CUDA_VISIBLE_DEVICES=-1 python example_python.py
```

---

## 📈 Benchmarks

### Python Directo (CPU)
- Embedding único: ~50ms
- 10 embeddings: ~300ms
- Búsqueda (100 items): ~5s

### API REST (CPU)
- Overhead de red: +10-20ms
- Throughput: mejor para batch

### GPU (si disponible)
- 10x más rápido que CPU
- Ideal para alta carga

---

## ❓ Troubleshooting

### Error: ModuleNotFoundError

```bash
pip install -r ../requirements.txt
```

### Error: Model not found

```bash
# Verificar que existe
ls -la ../model/model.safetensors
```

### Error: CUDA out of memory

```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
model = load_model("./model", device="cpu")
```

### Servidor API no inicia

```bash
# Verificar puerto disponible
netstat -an | grep 8000

# Usar puerto diferente
python ../api_wrapper.py --port 9000
```

---

## 📚 Recursos Adicionales

- **[README.md](../README.md)** - Documentación completa
- **[INTEGRACION.md](../INTEGRACION.md)** - Guía de integración
- **[MODEL_INFO.json](../MODEL_INFO.json)** - Metadata del modelo
- **[loader.py](../loader.py)** - Código fuente del loader
- **[api_wrapper.py](../api_wrapper.py)** - Código fuente de la API

---

## 💡 Tips Importantes

1. **Cache de embeddings** para textos repetidos
2. **Batch processing** para mejor rendimiento
3. **Considera GPU** si procesas muchos datos
4. **Monitorea memoria** en producción
5. **Usa la API** si necesitas múltiples clientes

---

## 📧 Soporte

Para dudas o problemas:

1. Revisa la documentación en [README.md](../README.md)
2. Consulta [INTEGRACION.md](../INTEGRACION.md)
3. Verifica los ejemplos en este directorio
4. Revisa los logs del servidor

---

*Última actualización: 8 de Enero, 2026*
