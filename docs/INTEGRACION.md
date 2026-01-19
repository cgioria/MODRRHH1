# 📚 GUÍA DE INTEGRACIÓN - MODELO PORTABLE

## 🎯 Introducción

Este documento explica cómo integrar el modelo entrenado en tus proyectos. El modelo está diseñado para ser portabilizable y puede usarse de múltiples formas:

1. **Como módulo Python** (integración directa)
2. **Como servicio API** (acceso remoto)
3. **Como contenedor Docker** (despliegue)

---

## 📦 Instalación

### Paso 1: Copiar los archivos

```bash
# Opción A: Copiar todo el directorio
cp -r modelo_entrenado_multiloss_portable /tu/proyecto/

# Opción B: Copiar solo lo necesario
cp -r modelo_entrenado_multiloss_portable/model /tu/proyecto/models/
cp modelo_entrenado_multiloss_portable/loader.py /tu/proyecto/
```

### Paso 2: Instalar dependencias

```bash
pip install -r modelo_entrenado_multiloss_portable/requirements.txt

# O mínimo:
pip install torch sentence-transformers numpy scikit-learn
```

### Paso 3: Verificar instalación

```bash
cd modelo_entrenado_multiloss_portable
python loader.py ./model test
```

---

## 🚀 Uso Básico (Módulo Python)

### Ejemplo 1: Generar Embeddings

```python
from loader import load_model

# Cargar modelo
model = load_model("./modelo_entrenado_multiloss_portable")

# Generar embedding para un texto
text = "desarrollador python con 5 años experiencia"
embedding = model.encode(text)

print(f"Dimensiones: {embedding.shape}")  # (768,)
print(f"Primeros 5: {embedding[:5]}")
```

### Ejemplo 2: Calcular Similitud

```python
from loader import load_model

model = load_model("./modelo_entrenado_multiloss_portable")

text1 = "python developer"
text2 = "python engineer"

similarity = model.similarity(text1, text2)
print(f"Similitud: {similarity:.4f}")  # 0.9979
```

### Ejemplo 3: Búsqueda

```python
from loader import load_model

model = load_model("./modelo_entrenado_multiloss_portable")

query = "python senior developer"
candidates = [
    "java programmer",
    "python engineer",
    "fullstack javascript",
    "python specialist"
]

results = model.search(query, candidates, top_k=2)

for r in results:
    print(f"{r['similarity']:.4f} - {r['candidate']}")
```

### Ejemplo 4: Clustering

```python
from loader import load_model

model = load_model("./modelo_entrenado_multiloss_portable")

texts = [
    "python developer",
    "python engineer",
    "java developer",
    "java programmer",
    "frontend react"
]

clusters = model.cluster(texts, n_clusters=3)

for cluster_id, group in clusters.items():
    print(f"Cluster {cluster_id}: {group}")
```

---

## 🌐 Uso como API

### Iniciar servidor

```bash
cd modelo_entrenado_multiloss_portable

# Opción 1: En puerto 8000
python api_wrapper.py

# Opción 2: Puerto personalizado
python api_wrapper.py --port 9000

# Opción 3: Con GPU
python api_wrapper.py --device cuda

# Opción 4: Desarrollo (reload automático)
python api_wrapper.py --reload
```

### Cliente Python (requests)

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Generar embeddings
response = requests.post(f"{BASE_URL}/embed", json={
    "texts": ["python developer", "java engineer"]
})
embeddings = response.json()

# 2. Calcular similitud
response = requests.post(f"{BASE_URL}/similarity", json={
    "text1": "python developer",
    "text2": "python engineer"
})
similarity = response.json()

# 3. Búsqueda
response = requests.post(f"{BASE_URL}/search", json={
    "query": "python developer",
    "candidates": ["java", "python engineer", "fullstack"],
    "top_k": 2
})
results = response.json()

# 4. Clustering
response = requests.post(f"{BASE_URL}/cluster", json={
    "texts": ["python", "java", "python engineer", "java dev"],
    "n_clusters": 2
})
clusters = response.json()
```

### Cliente cURL

```bash
# Embeddings
curl -X POST http://localhost:8000/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["python", "java"]}'

# Similitud
curl -X POST http://localhost:8000/similarity \
  -H "Content-Type: application/json" \
  -d '{"text1": "python", "text2": "python engineer"}'

# Búsqueda
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "python",
    "candidates": ["java", "python", "fullstack"]
  }'
```

### Cliente JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

async function search() {
  const response = await fetch('http://localhost:8000/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: 'python developer',
      candidates: ['java', 'python engineer', 'fullstack']
    })
  });
  
  const data = await response.json();
  console.log(data);
}

search();
```

---

## 🐳 Docker (Opcional)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "api_wrapper.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  modelo-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - TORCH_DEVICE=cpu
    volumes:
      - ./model:/app/model:ro
```

### Ejecutar

```bash
docker build -t modelo-api .
docker run -p 8000:8000 modelo-api
```

---

## 🔌 Integración en Proyectos Existentes

### Caso 1: Django

```python
# settings.py
from loader import load_model

MODELO = load_model("/path/to/modelo_entrenado_multiloss_portable")

# views.py
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

def buscar_candidatos(request):
    query = request.GET.get('q')
    candidates = [...lista de candidatos...]
    
    results = settings.MODELO.search(query, candidates, top_k=10)
    return JsonResponse(results, safe=False)
```

### Caso 2: Flask

```python
from flask import Flask, request, jsonify
from loader import load_model

app = Flask(__name__)
model = load_model("./modelo_entrenado_multiloss_portable")

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    results = model.search(
        data['query'],
        data['candidates'],
        data.get('top_k')
    )
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
```

### Caso 3: FastAPI (Standalone)

```python
# main.py
from fastapi import FastAPI
from loader import load_model

app = FastAPI()
model = load_model("./modelo_entrenado_multiloss_portable")

@app.post("/search")
async def search(query: str, candidates: list, top_k: int = None):
    return model.search(query, candidates, top_k)

# Ejecutar: uvicorn main:app --reload
```

### Caso 4: Streamlit

```python
# app.py
import streamlit as st
from loader import load_model

st.title("Búsqueda de Candidatos")

model = load_model("./modelo_entrenado_multiloss_portable")

query = st.text_input("Búsqueda:")
candidates = st.text_area("Candidatos (uno por línea)").split('\n')

if st.button("Buscar"):
    results = model.search(query, candidates)
    
    for r in results:
        st.write(f"{r['similarity']:.4f} - {r['candidate']}")

# Ejecutar: streamlit run app.py
```

---

## ⚙️ Configuración Avanzada

### Usar GPU

```python
from loader import load_model

# Usar CUDA
model = load_model("./modelo_entrenado_multiloss_portable", device="cuda")
```

### Batch Processing

```python
from loader import load_model
import numpy as np

model = load_model("./modelo_entrenado_multiloss_portable")

# Procesar muchos textos
texts = ["texto1", "texto2", ..., "textoN"]
embeddings = np.array([model.encode(text) for text in texts])

# O más eficiente:
embeddings = model.encode(texts)
```

### Cache de Embeddings

```python
from loader import load_model
import pickle

model = load_model("./modelo_entrenado_multiloss_portable")

# Cache
embedding_cache = {}

def get_embedding(text):
    if text not in embedding_cache:
        embedding_cache[text] = model.encode(text)
    return embedding_cache[text]

# Guardar cache
pickle.dump(embedding_cache, open('cache.pkl', 'wb'))
```

---

## 🔍 Troubleshooting

### Error: ModuleNotFoundError

```bash
pip install torch sentence-transformers
```

### Error: CUDA out of memory

```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Fuerza CPU
model = load_model("./model", device="cpu")
```

### Error: Model not found

```bash
# Verificar que existe
ls -la modelo_entrenado_multiloss_portable/model/

# Verificar archivos necesarios
ls modelo_entrenado_multiloss_portable/model/model.safetensors
```

### Modelo lento

```python
# Usar batch processing
embeddings = model.encode(["text1", "text2", "text3"])  # Más rápido

# Usar GPU si disponible
model = load_model("./model", device="cuda")
```

---

## 📊 Benchmarks

### Velocidad (CPU)

```
- Embedding único: ~50ms
- 10 embeddings: ~300ms
- Similitud: ~100ms
- Búsqueda (100 candidatos): ~5000ms
```

### Velocidad (GPU)

```
- Embedding único: ~5ms
- 10 embeddings: ~30ms
- Similitud: ~10ms
- Búsqueda (100 candidatos): ~500ms
```

---

## 📖 Documentación Completa

- **loader.py** - Módulo Python principal
- **api_wrapper.py** - API REST
- **MODEL_INFO.json** - Metadata del modelo
- **requirements.txt** - Dependencias

Accede a la documentación interactiva de la API en: `http://localhost:8000/docs`

---

## 🎓 Ejemplos Completos

Ver en el directorio `examples/`:
- `example_python.py` - Uso directo en Python
- `example_api.py` - Uso de API
- `example_django.py` - Integración Django
- `example_flask.py` - Integración Flask

---

## 💡 Tips

1. **Caché embeddings** si necesitas acceder a los mismos textos múltiples veces
2. **Usa batch processing** para mejor desempeño
3. **Considera GPU** si procesas muchos embeddings
4. **Monitorea memoria** en producción

---

*Última actualización: 8 de Enero, 2026*
