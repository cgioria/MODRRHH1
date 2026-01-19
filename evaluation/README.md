# 📊 EVALUACIÓN DE MODELO

Herramientas para medir y evaluar el rendimiento del modelo de recruitment.

## 📁 Contenido

```
evaluation/
├── evaluate_model.py                 # Script principal de evaluación
├── EVALUATION_REPORT.txt             # Reporte de evaluación
├── evaluation_results.json           # Resultados en JSON
├── HOW_TO_MEASURE_PERFORMANCE.py     # Guía de medición de rendimiento
├── QUICK_PERFORMANCE_TEST.py         # Test rápido de rendimiento
└── README.md                         # Este archivo
```

## 🚀 Uso Rápido

### 1. Evaluar el Modelo Completo

```bash
cd evaluation
python evaluate_model.py
```

**Salida esperada:**
```
INFERENCE SPEED:
  • 100 textos en 4.49 segundos
  • 22 textos/segundo
  • 44.85ms por texto

SIMILARITY METRICS:
  • Similitud media: 0.7702 ✅
  
SEARCH QUALITY:
  • MRR: 1.0000 ✅✅✅ EXCELENTE
  • NDCG: 0.9931 ✅✅✅ EXCELENTE
  
CLUSTERING:
  • Cohesión: 0.5427 ✅

MULTILINGUAL:
  • English: 0.8649 ✅
  • Spanish: 0.9482 ✅✅
  • ... y más
```

### 2. Test Rápido (1 minuto)

```bash
python QUICK_PERFORMANCE_TEST.py
```

Prueba solo velocidad e inferencia básica.

### 3. Ver Guía Completa

```bash
# Python
python HOW_TO_MEASURE_PERFORMANCE.py

# Markdown
cat EVALUATION_REPORT.txt
```

## 📈 Métricas Disponibles

| Métrica | Archivo | Descripción |
|---------|---------|-------------|
| Velocidad de Inferencia | `evaluate_model.py` | Textos por segundo, latencia |
| Similitud | `evaluate_model.py` | Score de similitud promedio |
| Búsqueda (MRR, NDCG) | `evaluate_model.py` | Calidad de ranking |
| Clustering | `evaluate_model.py` | Cohesión de grupos |
| Distribución de Embeddings | `evaluate_model.py` | Análisis de embeddings |
| Multilingüe | `evaluate_model.py` | Rendimiento en 5+ idiomas |

## 🔍 Interpretación de Resultados

### Velocidad
- ✅ Bueno: > 20 textos/seg en CPU
- ✅ Excelente: > 200 textos/seg en GPU

### Similitud
- ✅ Bueno: 0.7+ promedio
- ✅ Excelente: 0.8+ promedio

### Búsqueda (MRR)
- ✅ Bueno: > 0.8
- ✅ Excelente: > 0.95

### NDCG
- ✅ Bueno: > 0.9
- ✅ Excelente: > 0.98

## 📊 Archivo de Resultados

Los resultados se guardan automáticamente en:
- `evaluation_results.json` - Datos estructurados
- `EVALUATION_REPORT.txt` - Reporte formateado

## 🎯 Próximos Pasos

1. **Ejecutar evaluación inicial**
   ```bash
   python evaluate_model.py
   ```

2. **Revisar resultados**
   ```bash
   cat EVALUATION_REPORT.txt
   ```

3. **Guardar baseline**
   ```bash
   cp evaluation_results.json evaluation_results_baseline.json
   ```

4. **Comparar después de cambios**
   ```bash
   # Ejecutar nuevo test
   python evaluate_model.py
   # Comparar con baseline
   diff evaluation_results.json evaluation_results_baseline.json
   ```

## 🔧 Personalizar Evaluación

Edita `evaluate_model.py` para:
- Cambiar tamaño de muestra
- Agregar métricascustomizadas
- Evaluar dominios específicos
- Usar datos reales

## 📚 Información del Modelo

Evaluado: **paraphrase-multilingual-mpnet-base-v2**
- Dimensiones: 768
- Idiomas: 9
- Especialización: Recruitment
- MRR Actual: 1.0000
- NDCG Actual: 0.9931

---

**Última evaluación:** Ver `EVALUATION_REPORT.txt`
