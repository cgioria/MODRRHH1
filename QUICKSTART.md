# ⚡ QUICK START - 5 MINUTOS

## Opción 1: Python (30 segundos)

```bash
pip install -r requirements.txt

python -c "
from loader import load_model
model = load_model('./model')
print(model.similarity('python', 'java'))
"
```

---

## Opción 2: API (2 minutos)

**Terminal 1:**
```bash
python api_wrapper.py --port 8000
```

**Terminal 2:**
```bash
# Test
curl http://localhost:8000/health

# API docs (abre en navegador)
http://localhost:8000/docs
```

---

## Opción 3: Cliente (3 minutos)

```python
import requests

# Embeddings
r = requests.post('http://localhost:8000/embed', json={
    'texts': ['python developer', 'java engineer']
})
print(r.json())

# Similitud
r = requests.post('http://localhost:8000/similarity', json={
    'text1': 'python', 'text2': 'java'
})
print(r.json()['similarity'])

# Búsqueda
r = requests.post('http://localhost:8000/search', json={
    'query': 'python',
    'candidates': ['java', 'python', 'fullstack'],
    'top_k': 2
})
for item in r.json()['results']:
    print(f"{item['similarity']:.4f} - {item['candidate']}")
```

---

## Opción 4: Docker (1 minuto)

```bash
docker build -t modelo .
docker run -p 8000:8000 modelo
# Ya está en http://localhost:8000
```

---

## 📚 Lee Después

- **Más detalles**: README.md
- **Integración**: INTEGRACION.md
- **Deploy**: DEPLOYMENT.md
- **Índice**: INDICE.md
- **Ejemplos**: examples/

---

## ✅ Verificación Rápida

```bash
# Test del modelo
python loader.py ./model test

# Debe mostrar: ✅ Test 1-4 PASS
```

---

**¡Listo!** 🚀
