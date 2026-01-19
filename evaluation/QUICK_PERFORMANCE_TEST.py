"""
QUICK START: EVALUAR MODELO EN 5 MINUTOS
"""

# =========================================================================
# OPCIÓN 1: Evaluación completa automática (RECOMENDADO)
# =========================================================================

"""
Simplemente ejecuta:

    python evaluate_model.py ./model

Esto:
✓ Mide velocidad de inferencia
✓ Prueba similitud entre textos
✓ Evalúa calidad de búsqueda (ranking)
✓ Prueba clustering
✓ Analiza distribución de embeddings
✓ Prueba multilingüe
✓ Genera reporte en evaluation_results.json
"""


# =========================================================================
# OPCIÓN 2: Pruebas puntuales en Python
# =========================================================================

"""
Importar el evaluador:
"""

from evaluate_model import ModelEvaluator

# Crear evaluador
evaluator = ModelEvaluator("./model", device="cpu")


# Prueba 1: Velocidad
# ───────────────────
print("PRUEBA 1: Velocidad de procesamiento")
speed = evaluator.measure_inference_speed(num_texts=100)
print(f"  Velocidad: {speed['texts_per_second']:.0f} textos/segundo")
print(f"  Latencia: {speed['ms_per_text']:.2f} ms/texto\n")


# Prueba 2: Similitud
# ──────────────────
print("PRUEBA 2: Calidad de similitud")
similarity = evaluator.measure_similarity_metrics()
print(f"  Precisión: {similarity['accuracy_on_test_pairs']*100:.1f}%")
print(f"  Similitud media: {similarity['mean_similarity']:.4f}\n")


# Prueba 3: Búsqueda
# ─────────────────
print("PRUEBA 3: Calidad de ranking (búsqueda)")
search = evaluator.measure_search_quality()
print(f"  MRR: {search['mrr']:.4f}")
print(f"  NDCG: {search['ndcg']:.4f}")
print(f"  Precision@5: {search['precisions']['precision@5']:.4f}\n")


# Prueba 4: Clustering
# ───────────────────
print("PRUEBA 4: Calidad de clustering")
clustering = evaluator.measure_clustering_quality()
print(f"  Cohesión: {clustering['average_cohesion']:.4f}\n")


# Prueba 5: Todos juntos
# ──────────────────────
print("PRUEBA 5: Evaluación completa")
all_results = evaluator.run_full_evaluation()


# =========================================================================
# OPCIÓN 3: Pruebas específicas del dominio (Recruitment)
# =========================================================================

"""
Para evaluar específicamente para búsqueda de candidatos:
"""

from loader import load_model

model = load_model("./model")


# Test 1: Matching simple
# ──────────────────────
job_position = "Senior Python Developer with Machine Learning"
resume_text = "5 years python development, ml specialist"

score = model.similarity(job_position, resume_text)
print(f"Match score: {score:.2%}\n")


# Test 2: Búsqueda entre candidatos
# ─────────────────────────────────
query = "python backend engineer"

candidates = [
    "python developer 5 years backend",
    "java developer 10 years",
    "python engineer full stack",
    "frontend react developer",
    "devops kubernetes engineer",
]

results = model.search(query, candidates, top_k=3)

print("Top candidates:")
for i, result in enumerate(results, 1):
    print(f"  {i}. {result['candidate']}")
    print(f"     Score: {result['similarity']:.2%}\n")


# Test 3: Agrupación de perfiles
# ──────────────────────────────
profiles = [
    "python developer",
    "python engineer",
    "senior python programmer",
    "frontend developer react",
    "frontend developer vue",
    "data scientist ml",
    "data engineer spark",
    "devops engineer",
]

clusters = model.cluster(profiles, n_clusters=4)

print("Clusters de perfiles:")
for cluster_id, group in clusters.items():
    print(f"\nGrupo {cluster_id}:")
    for profile in group:
        print(f"  - {profile}")


# =========================================================================
# OPCIÓN 4: Evaluar versus baseline
# =========================================================================

"""
Comparar con otro modelo (baseline):
"""

from sentence_transformers import SentenceTransformer

# Tu modelo entrenado
trained_model = load_model("./model")

# Modelo base sin entrenar
base_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# Test pair
text1 = "python developer"
text2 = "python engineer"

score_trained = trained_model.similarity(text1, text2)
score_base = base_model.similarity(text1, text2)

print(f"Similitud '{text1}' vs '{text2}':")
print(f"  Modelo base:     {score_base:.4f}")
print(f"  Modelo entrenado: {score_trained:.4f}")
print(f"  Mejora:          +{(score_trained - score_base):.4f} ({(score_trained/score_base - 1)*100:.1f}%)")


# =========================================================================
# OPCIÓN 5: Tests con datos reales
# =========================================================================

"""
Si tienes datos reales de tu dominio:
"""

# Ejemplo: CVs y descripciones de puestos
real_candidates = [
    "Ingeniero de software con 10 años en Python",
    "Desarrollador backend en Java y Spring",
    "Científico de datos especializado en ML",
    "Arquitecto de soluciones cloud",
]

real_positions = [
    "Buscamos developer senior python",
    "Necesitamos ingeniero backend java",
    "Requerimos data scientist ml engineer",
]

print("Matching Job <-> Candidate:\n")
for position in real_positions:
    print(f"Posición: {position}")
    results = model.search(position, real_candidates, top_k=2)
    for r in results:
        print(f"  ✓ {r['candidate']} ({r['similarity']:.1%})")
    print()


# =========================================================================
# OPCIÓN 6: Guardar y visualizar resultados
# =========================================================================

"""
Guardar evaluación completa:
"""

evaluator = ModelEvaluator("./model")
results = evaluator.run_full_evaluation()
evaluator.save_results("my_evaluation.json")

# Los resultados están en my_evaluation.json

import json

with open("my_evaluation.json") as f:
    results = json.load(f)

# Ver las métricas principales
print(json.dumps(results, indent=2))


# =========================================================================
# BENCHMARK: COMPARATIVA DE RESULTADOS
# =========================================================================

"""
Tabla de referencia de buenos resultados:

╔══════════════════════════════╦═══════════════╦══════════════╦═══════════╗
║ Métrica                      ║ Excelente (✅) ║ Bueno (🟡)    ║ Revisar (❌)║
╠══════════════════════════════╬═══════════════╬══════════════╬═══════════╣
║ Velocidad (CPU textos/seg)  ║ > 200         ║ 50-200       ║ < 50      ║
║ Velocidad (GPU textos/seg)  ║ > 1000        ║ 500-1000     ║ < 500     ║
║ Similitud accuracy          ║ > 80%         ║ 60-80%       ║ < 60%     ║
║ MRR (Mean Reciprocal Rank)  ║ > 0.8         ║ 0.5-0.8      ║ < 0.5     ║
║ NDCG (Normalized DCG)       ║ > 0.75        ║ 0.5-0.75     ║ < 0.5     ║
║ Precision@5                 ║ > 0.8         ║ 0.6-0.8      ║ < 0.6     ║
║ Clustering cohesion         ║ > 0.7         ║ 0.5-0.7      ║ < 0.5     ║
╚══════════════════════════════╩═══════════════╩══════════════╩═══════════╝
"""


# =========================================================================
# INTERPRETACIÓN DE RESULTADOS
# =========================================================================

"""
Según tus métricas de entrenamiento en MODEL_INFO.json:

✅ Tu modelo mostró:
  • +33.05% mejora vs modelo original en similarity pairs
  • Similitud promedio: 0.8795 (vs 0.5490 original)
  • Exactitud en triplets: 80%

Esto significa que:
  1. Es EXCELENTE para búsqueda y ranking
  2. Los embeddings son discriminativos
  3. Distingue bien entre candidatos similares y diferentes

Próximos pasos:
  1. Ejecutar evaluate_model.py para verificar en tu máquina
  2. Si hay discrepancias, revisar los datos de test
  3. Considerar fine-tuning adicional si es necesario
"""


# =========================================================================
# MÁS INFORMACIÓN
# =========================================================================

"""
Para más detalles, ver:
  • HOW_TO_MEASURE_PERFORMANCE.py (esta guía completa)
  • evaluate_model.py (script de evaluación)
  • README.md (documentación principal)
  • CHECKLIST.md (verificaciones)
"""
