# 🤖 AGENTES DE RECRUITMENT

Este directorio contiene todos los agentes y documentación para el sistema de recruitment.

## 📁 Estructura

```
agent/
├── agents_simple.py              # Agente simple con reglas (comienza aquí)
├── agents_advanced.py            # Agente avanzado con herramientas
├── agent_api.py                  # API REST con FastAPI
├── AGENT_GUIDE.md                # Guía completa
├── AGENTS_SUMMARY.md             # Resumen ejecutivo
├── QUICK_AGENT_REFERENCE.py      # Referencia rápida
└── README.md                      # Este archivo
```

## ⚠️ Importante: UN SOLO MODELO

**No hay dos modelos.** Todos los agentes usan el **mismo modelo entrenado** ubicado en:
```
../model/
```

Los agentes buscan automáticamente la ruta del modelo, por lo que puedes ejecutarlos desde cualquier ubicación:

```bash
# Desde la carpeta agent/
python agents_simple.py

# O desde el directorio raíz
python agent/agents_simple.py

# O desde cualquier lugar (si tienes las rutas correctas)
python path/to/agent/agents_simple.py
```

## 🚀 Cómo empezar

### Opción 1: Agente Simple (5 minutos)
```bash
python agents_simple.py
```
Prueba funcionalidades básicas: búsqueda, matching, similitud, clustering.

### Opción 2: Agente Avanzado
```bash
python agents_advanced.py
```
Más funcionalidades con gestión de estado y memoria.

### Opción 3: API REST (30 minutos)
```bash
pip install fastapi uvicorn
uvicorn agent_api:app --reload --port 8000
```
Luego accede a: `http://localhost:8000/docs`

## 📚 Documentación

- **AGENT_GUIDE.md** - Guía completa sobre tipos de agentes
- **AGENTS_SUMMARY.md** - Resumen ejecutivo
- **QUICK_AGENT_REFERENCE.py** - Ejemplos rápidos
- **../FINAL_SUMMARY.txt** - Resumen visual del proyecto

## 🔧 Modelo Usado

**Todos los agentes usan el mismo modelo:**
- Nombre: `paraphrase-multilingual-mpnet-base-v2`
- Ubicación: `../model/`
- Dimensiones: 768
- Especialización: Recruitment
- Idiomas: 9 (English, Spanish, Portuguese, French, German, Italian, Dutch, Romanian, Chinese)

### Rendimiento del Modelo
- MRR: 1.0000 (ranking perfecto)
- NDCG: 0.9931 (casi óptimo)
- Velocidad: 22 textos/seg en CPU
- Multilingüe: 91% de promedio

## 💡 Tips

1. **Sin duplicados**: Solo hay UN modelo, todos lo usan
2. **Rutas automáticas**: Los agentes encuentran automáticamente la ruta del modelo
3. **Sin dependencias extra**: El agente simple solo necesita `loader.py`
4. **Escalable**: El agente API es production-ready

## 📝 Próximos pasos

1. ✅ Ejecuta `agents_simple.py` para verificar que funciona
2. 📊 Personaliza con tus datos (actualiza `candidates_db` y `jobs_db`)
3. 💾 Integra con base de datos real (PostgreSQL)
4. 🚀 Despliega como API
5. 📈 Monitorea y optimiza

---

**Nota**: Los agentes cargan automáticamente desde `../model/`. No necesitas hacer nada especial.
