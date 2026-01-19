"""
GUÍA: CÓMO MEDIR EL RENDIMIENTO DEL MODELO
"""

import os
import json
from pathlib import Path

# =========================================================================
# RESUMEN EJECUTIVO
# =========================================================================

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                 CÓMO MEDIR EL RENDIMIENTO DEL MODELO                 ║
╚═══════════════════════════════════════════════════════════════════════╝

Tu modelo es un Sentence Transformer entrenado con:
  • Base model: paraphrase-multilingual-mpnet-base-v2 (768 dimensiones)
  • Pérdidas: CosineSimilarityLoss + TripletLoss + MultipleNegativesRankingLoss
  • Dominio: Búsqueda y ranking de candidatos (Recruitment)
  • Datos: 10,000 ejemplos en 3 épocas

═══════════════════════════════════════════════════════════════════════

1️⃣  MÉTRICAS DE VELOCIDAD (Latencia)
────────────────────────────────────────

   Qué mide: Cuánto tiempo tarda en procesar textos

   Código:
   ```python
   from evaluate_model import ModelEvaluator
   
   evaluator = ModelEvaluator("./model", device="cpu")
   speed = evaluator.measure_inference_speed(num_texts=1000)
   
   print(speed["texts_per_second"])  # textos procesados por segundo
   print(speed["ms_per_text"])       # milisegundos por texto
   ```

   Benchmarks esperados:
   • CPU: 50-200 textos/segundo
   • GPU (CUDA): 500-2000 textos/segundo

   Factores que afectan:
   - Dispositivo (CPU vs GPU)
   - Longitud de los textos
   - Batch size

═══════════════════════════════════════════════════════════════════════

2️⃣  MÉTRICAS DE SIMILITUD (Calidad de Embeddings)
────────────────────────────────────────────────

   Qué mide: Qué tan bien distingue textos similares de diferentes

   Código:
   ```python
   evaluator.measure_similarity_metrics()
   ```

   Métricas clave:
   • Similitud media: ¿Cuán similares son los embeddings en general?
   • Desv. estándar: ¿Hay buena dispersión?
   • Precisión en test pairs: % de pares clasificados correctamente

   Interpretación:
   - Similitud media > 0.7:  ✅ Muy bueno
   - Similitud media 0.5-0.7: ⚠️  Aceptable
   - Similitud media < 0.5:  ❌ Revisar

   Ejemplo de salida esperada:
   • Textos iguales: similitud ≈ 0.95-1.0
   • Textos similares: similitud ≈ 0.7-0.9
   • Textos diferentes: similitud ≈ 0.2-0.5

═══════════════════════════════════════════════════════════════════════

3️⃣  MÉTRICAS DE BÚSQUEDA (Ranking)
──────────────────────────────────

   Qué mide: Qué tan bien rankea candidatos por relevancia

   Código:
   ```python
   evaluator.measure_search_quality()
   ```

   Métricas estándar:
   
   📌 MRR (Mean Reciprocal Rank):
      ¿En qué posición encuentra el primer resultado relevante?
      Rango: 0-1 (1 es perfecto)
      • MRR > 0.8: ✅ Excelente
      • MRR 0.5-0.8: ⚠️  Bueno
      • MRR < 0.5: ❌ Pobre

   📌 NDCG (Normalized Discounted Cumulative Gain):
      Combina posición y relevancia de resultados
      Rango: 0-1 (1 es perfecto)
      • NDCG > 0.75: ✅ Excelente
      • NDCG 0.5-0.75: ⚠️  Bueno
      • NDCG < 0.5: ❌ Pobre

   📌 Precision@k:
      % de resultados relevantes en los top-k
      • Precision@5 > 0.6: ✅ Bueno
      • Precision@10 > 0.5: ✅ Bueno

   Ejemplo:
   Query: "senior python developer with ml"
   
   Resultados:
   1. "python developer 5 years" - RELEVANTE
   2. "senior python engineer ml" - RELEVANTE
   3. "java developer 10 years" - NO RELEVANTE
   4. "python ml specialist" - RELEVANTE
   5. "frontend developer" - NO RELEVANTE
   
   → MRR = 1/1 = 1.0 ✅
   → Precision@5 = 3/5 = 0.6 ✅

═══════════════════════════════════════════════════════════════════════

4️⃣  MÉTRICAS DE CLUSTERING
───────────────────────────

   Qué mide: Qué tan bien agrupa textos similares

   Código:
   ```python
   evaluator.measure_clustering_quality()
   ```

   Métrica principal:
   • Cohesión (average cohesion):
     Similitud media dentro de cada cluster
     Rango: 0-1
     • Cohesión > 0.7: ✅ Excelente
     • Cohesión 0.5-0.7: ⚠️  Bueno
     • Cohesión < 0.5: ❌ Revisar

═══════════════════════════════════════════════════════════════════════

5️⃣  ANÁLISIS DE EMBEDDINGS
───────────────────────────

   Qué mide: Propiedades de los vectores generados

   Código:
   ```python
   evaluator.measure_embedding_distribution()
   ```

   Verificar:
   • Norma (magnitud):
     - Deberían estar normalizadas (norm ≈ 1)
     - Si norm << 1 o >> 1, revisar

   • Similitud entre embeddings aleatorios:
     - Deberían estar distribuidas
     - Si media de similitud es muy alta (> 0.9), embeddings colapsan

   • Eigenvalores (PCA):
     - Muestran cuántas dimensiones son efectivas
     - Si uno domina mucho, hay sesgos

═══════════════════════════════════════════════════════════════════════

6️⃣  EVALUACIÓN MULTILINGÜE
────────────────────────────

   Qué mide: Rendimiento en diferentes idiomas

   Código:
   ```python
   evaluator.measure_multilingual_performance()
   ```

   Tu modelo soporta:
   English, Spanish, Portuguese, French, German, Italian, Dutch, 
   Romanian, Chinese

   Verificar que la similitud sea consistente entre idiomas

═══════════════════════════════════════════════════════════════════════

📊 CÓMO EJECUTAR LA EVALUACIÓN COMPLETA
─────────────────────────────────────────

   Opción 1: Script directo
   ───────────────────────
   python evaluate_model.py ./model

   Opción 2: En Python
   ──────────────────
   from evaluate_model import ModelEvaluator
   
   evaluator = ModelEvaluator("./model", device="cpu")
   results = evaluator.run_full_evaluation()

   Opción 3: Pruebas individuales
   ──────────────────────────────
   from evaluate_model import ModelEvaluator
   
   evaluator = ModelEvaluator("./model")
   
   # Una métrica a la vez
   speed = evaluator.measure_inference_speed(100)
   similarity = evaluator.measure_similarity_metrics()
   search = evaluator.measure_search_quality()
   # ... etc

═══════════════════════════════════════════════════════════════════════

📈 INTERPRETAR LOS RESULTADOS
──────────────────────────────

   EXCELENTE (✅ Verde):
   • Velocidad: > 200 textos/seg (CPU) o > 1000 (GPU)
   • Similitud: precisión > 80%
   • MRR > 0.8
   • NDCG > 0.75
   • Cohesión > 0.7

   BUENO (🟡 Amarillo):
   • Velocidad: 50-200 textos/seg (CPU)
   • Similitud: precisión 60-80%
   • MRR 0.5-0.8
   • NDCG 0.5-0.75
   • Cohesión 0.5-0.7

   A REVISAR (❌ Rojo):
   • Velocidad: < 50 textos/seg (CPU)
   • Similitud: precisión < 60%
   • MRR < 0.5
   • NDCG < 0.5
   • Cohesión < 0.5

═══════════════════════════════════════════════════════════════════════

🔍 PRUEBAS ESPECÍFICAS POR CASO DE USO
───────────────────────────────────────

   CASO 1: Búsqueda de candidatos
   ────────────────────────────────
   
   from loader import load_model
   
   model = load_model("./model")
   
   # Buscar candidatos para una posición
   position = "senior python developer"
   candidates = [
       "python developer 5 years",
       "java developer 10 years",
       "python engineer with ml",
       "frontend developer react",
       "senior backend python engineer"
   ]
   
   results = model.search(position, candidates, top_k=3)
   for r in results:
       print(f"{r['candidate']}: {r['similarity']:.2%}")

   CASO 2: Agrupación de CVs
   ──────────────────────────
   
   resumes = [...]  # Cientos de CVs
   clusters = model.cluster(resumes, n_clusters=10)
   
   # Ahora tienes grupos de perfiles similares

   CASO 3: Matching Job-Candidate
   ───────────────────────────────
   
   job_desc = "Looking for senior backend engineer"
   resume = "5 years python development experience"
   
   match_score = model.similarity(job_desc, resume)
   print(f"Match score: {match_score:.2%}")

═══════════════════════════════════════════════════════════════════════

💡 TIPS DE OPTIMIZACIÓN
────────────────────────

   1. Para mejorar velocidad:
      • Usar GPU (CUDA) si está disponible
      • Aumentar batch size en inference
      • Usar quantization (convertir a int8)

   2. Para mejorar similitud:
      • Fine-tuning adicional con más datos
      • Ajustar pérdidas de entrenamiento
      • Aumentar épocas

   3. Para mejorar ranking:
      • Revisar dataset de entrenamiento
      • Usar hard negatives
      • Ajustar threshold de similitud

═══════════════════════════════════════════════════════════════════════

📁 ARCHIVOS RELACIONADOS
─────────────────────────

   • evaluate_model.py      - Script de evaluación completo
   • loader.py             - Cargador del modelo
   • MODEL_INFO.json       - Información del modelo
   • examples/             - Ejemplos de uso

═══════════════════════════════════════════════════════════════════════
""")
