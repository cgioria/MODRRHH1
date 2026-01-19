# 📦 GUÍA POST-CLONE

Después de clonar el repositorio, sigue estos pasos:

## ⚡ Opción A: Setup Automático (Recomendado)

### Windows
```bash
setup.bat
```

### Linux / Mac
```bash
bash setup.sh
```

Esto hará:
- ✅ Crear virtual environment
- ✅ Instalar todas las dependencias
- ✅ Descargar archivos grandes (Git LFS)
- ✅ Verificar que todo funciona
- ✅ Mostrar próximos pasos

---

## 🔧 Opción B: Setup Manual (Si lo anterior no funciona)

### 1. Instalar Git LFS (IMPORTANTE)
```bash
# Descargar desde: https://git-lfs.com/
# O en Linux: sudo apt install git-lfs
# O en Mac: brew install git-lfs
```

### 2. Descargar Archivos Grandes
```bash
git lfs pull
```

### 3. Crear Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5. Verificar Setup
```bash
python setup_check.py
```

---

## ✅ Verificación Rápida

```bash
python -c "
from loader import load_model
model = load_model('./model')
print('✅ Modelo cargado correctamente')
print(f'   Dimensiones: 768')
print(f'   Idiomas: 9 (English, Spanish, Portuguese, etc.)')
"
```

---

## 🚀 Primeros Pasos

Una vez verificado, elige tu opción:

### A) Agente Simple (5 segundos)
```bash
python agent/agents_simple.py
```

### B) API REST (10 segundos)
```bash
uvicorn agent.agent_api:app --reload --port 8000
# Acceder a: http://localhost:8000/docs
```

### C) Docker (1 minuto)
```bash
docker build -t recruitment-model .
docker run -p 8000:8000 recruitment-model
# Acceder a: http://localhost:8000
```

### D) Ejemplos Python
```bash
python examples/python/example_python.py
python examples/api/example_api_client.py
```

---

## 📚 Documentación

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Visión general del proyecto |
| `QUICKSTART.md` | 5 opciones rápidas para empezar |
| `agent/README.md` | Guía de agentes |
| `docs/ARCHITECTURE.md` | Arquitectura técnica (1500 líneas) |
| `deployment/README.md` | Deployment en producción |
| `evaluation/README.md` | Cómo medir performance |

---

## ⚠️ Solución de Problemas

### Git LFS necesario
```
Error: model/model.safetensors no encontrado
Solución: Instalar Git LFS y ejecutar: git lfs pull
```

### Dependencias faltantes
```
Error: ModuleNotFoundError: No module named 'torch'
Solución: pip install -r requirements.txt
```

### Puerto 8000 ya en uso
```
Error: Address already in use
Solución: uvicorn agent.agent_api:app --reload --port 8001
```

### Python 3.8+ necesario
```
Error: Syntax error (f-strings no soportados)
Solución: Instalar Python 3.8+ desde https://www.python.org/
```

---

## 🎯 Próximos Pasos Recomendados

1. **Leer**: README.md para entender el proyecto
2. **Probar**: Ejecutar setup_check.py para verificar
3. **Experimentar**: Ejecutar agent/agents_simple.py
4. **Integrar**: Ver ejemplos en examples/
5. **Deployer**: Seguir deployment/README.md

---

## 🆘 Ayuda

- 📖 Documentación: `docs/INDEX.md`
- 💬 Ver ejemplos: `examples/README.md`
- 🐳 Deploy con Docker: `deployment/README.md`
- 📊 Evaluar modelo: `evaluation/README.md`

---

## ✨ ¡Listo!

Una vez completado el setup:
- ✅ Proyecto completamente funcional
- ✅ Modelo cargado y listo
- ✅ Agentes disponibles
- ✅ API funcionando
- ✅ Documentación accesible

**¡A programar! 🚀**
