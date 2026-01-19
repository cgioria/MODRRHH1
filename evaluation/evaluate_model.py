"""
SCRIPT DE EVALUACIÓN DEL MODELO
Mide el rendimiento del modelo en diferentes aspectos
"""

import os
import json
import time
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
from sklearn.metrics.pairwise import cosine_similarity
from loader import load_model


class ModelEvaluator:
    """Evaluador completo del modelo"""
    
    def __init__(self, model_path: str, device: str = "cpu"):
        """Inicializar evaluador"""
        self.model = load_model(model_path, device=device)
        self.results = {}
        print("🔍 Evaluador de Modelo inicializado\n")
    
    # =========================================================================
    # 1. MÉTRICAS DE VELOCIDAD
    # =========================================================================
    
    def measure_inference_speed(self, num_texts: int = 1000) -> Dict:
        """Medir velocidad de inferencia"""
        print("⏱️  Midiendo velocidad de inferencia...")
        
        # Textos de prueba
        test_texts = [
            f"python developer with {i} years experience"
            for i in range(num_texts)
        ]
        
        # Medir tiempo
        start = time.time()
        embeddings = self.model.encode(test_texts)
        elapsed = time.time() - start
        
        # Calcular métricas
        texts_per_second = num_texts / elapsed
        ms_per_text = (elapsed / num_texts) * 1000
        
        results = {
            "total_texts": num_texts,
            "total_time_seconds": elapsed,
            "texts_per_second": texts_per_second,
            "ms_per_text": ms_per_text,
            "embeddings_shape": embeddings.shape,
        }
        
        print(f"  ✓ {num_texts} textos en {elapsed:.2f}s")
        print(f"  ✓ {texts_per_second:.0f} textos/segundo")
        print(f"  ✓ {ms_per_text:.2f}ms por texto\n")
        
        self.results["inference_speed"] = results
        return results
    
    # =========================================================================
    # 2. MÉTRICAS DE SIMILITUD
    # =========================================================================
    
    def measure_similarity_metrics(self) -> Dict:
        """Medir calidad de similitud con pares de ejemplo"""
        print("📊 Midiendo métricas de similitud...")
        
        # Pares de textos: (texto1, texto2, similitud_esperada)
        test_pairs = [
            # Muy similares (esperado > 0.8)
            ("python developer", "python engineer", 0.9),
            ("java developer", "java programmer", 0.9),
            ("senior developer", "senior engineer", 0.85),
            
            # Similares (esperado 0.5-0.8)
            ("frontend developer", "backend developer", 0.7),
            ("data scientist", "machine learning engineer", 0.7),
            ("project manager", "scrum master", 0.6),
            
            # No muy similares (esperado 0.2-0.5)
            ("python developer", "marketing manager", 0.3),
            ("cloud engineer", "accountant", 0.2),
            ("devops engineer", "graphic designer", 0.2),
        ]
        
        similarities = []
        distances = []
        
        for text1, text2, expected in test_pairs:
            sim = self.model.similarity(text1, text2)
            similarities.append({
                "pair": (text1, text2),
                "similarity": sim,
                "expected_range": expected,
                "correct": abs(sim - expected) < 0.15  # ±0.15 margen
            })
            distances.append(sim)
        
        # Estadísticas
        similarities_arr = np.array([s["similarity"] for s in similarities])
        accuracy = np.mean([s["correct"] for s in similarities])
        
        results = {
            "test_pairs": len(test_pairs),
            "similarity_scores": distances,
            "mean_similarity": float(np.mean(similarities_arr)),
            "std_similarity": float(np.std(similarities_arr)),
            "min_similarity": float(np.min(similarities_arr)),
            "max_similarity": float(np.max(similarities_arr)),
            "accuracy_on_test_pairs": float(accuracy),
            "test_results": [
                {
                    "pair": f"{s['pair'][0]} <-> {s['pair'][1]}",
                    "similarity": round(s['similarity'], 4),
                    "expected": s['expected_range'],
                    "correct": s['correct']
                }
                for s in similarities
            ]
        }
        
        print(f"  ✓ {len(test_pairs)} pares evaluados")
        print(f"  ✓ Similitud media: {results['mean_similarity']:.4f}")
        print(f"  ✓ Precisión en test: {accuracy*100:.1f}%")
        print(f"  ✓ Rango: [{results['min_similarity']:.4f}, {results['max_similarity']:.4f}]\n")
        
        self.results["similarity_metrics"] = results
        return results
    
    # =========================================================================
    # 3. MÉTRICAS DE BUSQUEDA Y RANKING
    # =========================================================================
    
    def measure_search_quality(self) -> Dict:
        """Evaluar calidad de búsqueda (ranking)"""
        print("🔎 Evaluando calidad de búsqueda...")
        
        # Query
        query = "senior python developer with machine learning experience"
        
        # Candidatos (algunos relevantes, otros no)
        candidates = [
            "python developer 5 years experience",
            "senior python engineer ml",
            "java developer 10 years",
            "python and machine learning specialist",
            "data scientist with python",
            "frontend developer javascript",
            "senior ml engineer tensorflow",
            "devops engineer kubernetes",
            "python backend developer",
            "marketing manager"
        ]
        
        # Buscar
        results = self.model.search(query, candidates, top_k=len(candidates))
        
        # Relevancia manual (1=relevante, 0=no relevante)
        relevance = {
            "python developer 5 years experience": 1,
            "senior python engineer ml": 1,
            "java developer 10 years": 0,
            "python and machine learning specialist": 1,
            "data scientist with python": 1,
            "frontend developer javascript": 0,
            "senior ml engineer tensorflow": 1,
            "devops engineer kubernetes": 0,
            "python backend developer": 1,
            "marketing manager": 0
        }
        
        # Calcular MRR (Mean Reciprocal Rank)
        mrr = 0
        for i, result in enumerate(results):
            if relevance.get(result["candidate"], 0) == 1:
                mrr = 1 / (i + 1)
                break
        
        # Calcular NDCG (Normalized Discounted Cumulative Gain)
        dcg = 0
        for i, result in enumerate(results):
            rel = relevance.get(result["candidate"], 0)
            dcg += rel / np.log2(i + 2)  # +2 para evitar log2(1)
        
        # IDCG (ideal DCG - si todos relevantes están en top)
        relevant_count = sum(1 for v in relevance.values() if v == 1)
        idcg = sum(1 / np.log2(i + 2) for i in range(relevant_count))
        ndcg = dcg / idcg if idcg > 0 else 0
        
        # Precision@k
        k_values = [3, 5, 10]
        precisions = {}
        for k in k_values:
            top_k = results[:k]
            relevant_in_top_k = sum(1 for r in top_k if relevance.get(r["candidate"], 0) == 1)
            precisions[f"precision@{k}"] = relevant_in_top_k / k
        
        results_dict = {
            "query": query,
            "candidates_count": len(candidates),
            "relevant_count": relevant_count,
            "mrr": float(mrr),
            "ndcg": float(ndcg),
            "precisions": {k: float(v) for k, v in precisions.items()},
            "top_results": [
                {
                    "rank": i + 1,
                    "candidate": r["candidate"],
                    "similarity": round(r["similarity"], 4),
                    "relevant": bool(relevance.get(r["candidate"], 0))
                }
                for i, r in enumerate(results[:5])
            ]
        }
        
        print(f"  ✓ Query: {query}")
        print(f"  ✓ MRR (Mean Reciprocal Rank): {mrr:.4f}")
        print(f"  ✓ NDCG: {ndcg:.4f}")
        for k, p in precisions.items():
            print(f"  ✓ {k}: {p:.4f}")
        print()
        
        self.results["search_quality"] = results_dict
        return results_dict
    
    # =========================================================================
    # 4. MÉTRICAS DE CLUSTERING
    # =========================================================================
    
    def measure_clustering_quality(self) -> Dict:
        """Evaluar clustering de textos"""
        print("🎯 Evaluando calidad de clustering...")
        
        texts = [
            # Cluster 1: Python developers
            "python developer 5 years",
            "senior python engineer",
            "python programmer",
            
            # Cluster 2: Frontend developers
            "frontend developer javascript",
            "react developer",
            "vue.js developer",
            
            # Cluster 3: Data roles
            "data scientist",
            "machine learning engineer",
            "data engineer",
        ]
        
        # Realizar clustering
        clusters = self.model.cluster(texts, n_clusters=3)
        
        # Calcular cohesión (similitud media dentro de cluster)
        embeddings = np.array([self.model.encode(text) for text in texts])
        
        cohesion_scores = []
        for cluster_id, cluster_texts in clusters.items():
            if len(cluster_texts) < 2:
                continue
            
            cluster_indices = [texts.index(t) for t in cluster_texts]
            cluster_embeddings = embeddings[cluster_indices]
            
            # Similitud media dentro del cluster
            if len(cluster_embeddings) > 1:
                pairwise_sims = cosine_similarity(cluster_embeddings)
                # Media de similitudes (excluir diagonal)
                np.fill_diagonal(pairwise_sims, 0)
                cohesion = np.mean(pairwise_sims)
                cohesion_scores.append(cohesion)
        
        avg_cohesion = np.mean(cohesion_scores) if cohesion_scores else 0
        
        results_dict = {
            "texts_count": len(texts),
            "clusters_count": len(clusters),
            "average_cohesion": float(avg_cohesion),
            "clusters": {
                f"cluster_{k}": cluster_texts
                for k, cluster_texts in clusters.items()
            }
        }
        
        print(f"  ✓ {len(texts)} textos en {len(clusters)} clusters")
        print(f"  ✓ Cohesión media: {avg_cohesion:.4f}\n")
        
        self.results["clustering_quality"] = results_dict
        return results_dict
    
    # =========================================================================
    # 5. ANÁLISIS DE DISTRIBUCIÓN DE EMBEDDINGS
    # =========================================================================
    
    def measure_embedding_distribution(self) -> Dict:
        """Analizar distribución de embeddings"""
        print("📈 Analizando distribución de embeddings...")
        
        texts = [
            "python developer", "java developer", "frontend developer",
            "data scientist", "machine learning engineer", "devops engineer",
            "senior software engineer", "junior developer", "architect",
            "technical lead", "engineering manager", "product manager",
        ]
        
        embeddings = np.array([self.model.encode(text) for text in texts])
        
        # Estadísticas
        mean_norm = np.linalg.norm(embeddings, axis=1).mean()
        std_norm = np.linalg.norm(embeddings, axis=1).std()
        
        # Similitud media entre todos los pares
        pairwise_sims = cosine_similarity(embeddings)
        np.fill_diagonal(pairwise_sims, 0)
        mean_similarity = pairwise_sims.mean()
        
        # Eigenvalores de la matriz de covarianza (PCA)
        cov_matrix = np.cov(embeddings.T)
        eigenvalues = np.linalg.eigvals(cov_matrix)
        explained_variance = sorted(eigenvalues, reverse=True)[:5]
        
        results_dict = {
            "embeddings_count": len(texts),
            "embedding_dimension": embeddings.shape[1],
            "norm_statistics": {
                "mean": float(mean_norm),
                "std": float(std_norm),
                "min": float(np.linalg.norm(embeddings, axis=1).min()),
                "max": float(np.linalg.norm(embeddings, axis=1).max()),
            },
            "similarity_statistics": {
                "mean": float(mean_similarity),
                "std": float(pairwise_sims.std()),
                "min": float(pairwise_sims.min()),
                "max": float(pairwise_sims.max()),
            },
            "top_5_eigenvalues": [float(v) for v in explained_variance],
        }
        
        print(f"  ✓ {len(texts)} embeddings analizados")
        print(f"  ✓ Norma media: {mean_norm:.4f} ± {std_norm:.4f}")
        print(f"  ✓ Similitud media: {mean_similarity:.4f}")
        print(f"  ✓ Dimensiones efectivas (varianza): {sum(explained_variance):.2f}\n")
        
        self.results["embedding_distribution"] = results_dict
        return results_dict
    
    # =========================================================================
    # 6. EVALUACIÓN MULTILINGÜE
    # =========================================================================
    
    def measure_multilingual_performance(self) -> Dict:
        """Evaluar rendimiento en diferentes idiomas"""
        print("🌍 Evaluando rendimiento multilingüe...")
        
        # Pares en diferentes idiomas
        test_pairs = [
            # English
            ("python developer", "python engineer", "english"),
            # Spanish
            ("desarrollador python", "ingeniero python", "spanish"),
            # Portuguese
            ("desenvolvedor python", "engenheiro python", "portuguese"),
            # French
            ("développeur python", "ingénieur python", "french"),
            # German
            ("Python-Entwickler", "Python-Ingenieur", "german"),
        ]
        
        results_by_lang = {}
        
        for text1, text2, lang in test_pairs:
            try:
                sim = self.model.similarity(text1, text2)
                if lang not in results_by_lang:
                    results_by_lang[lang] = []
                results_by_lang[lang].append(sim)
            except Exception as e:
                print(f"  ⚠️  Error con {lang}: {e}")
        
        results_dict = {
            "languages_tested": len(results_by_lang),
            "language_performance": {
                lang: {
                    "similarity_scores": [float(s) for s in sims],
                    "mean": float(np.mean(sims)),
                    "std": float(np.std(sims)) if len(sims) > 1 else 0.0,
                }
                for lang, sims in results_by_lang.items()
            }
        }
        
        print(f"  ✓ {len(results_by_lang)} idiomas evaluados")
        for lang, stats in results_dict["language_performance"].items():
            print(f"  ✓ {lang}: media {stats['mean']:.4f}")
        print()
        
        self.results["multilingual"] = results_dict
        return results_dict
    
    # =========================================================================
    # 7. RESUMEN EJECUTIVO
    # =========================================================================
    
    def generate_summary_report(self) -> Dict:
        """Generar reporte completo"""
        print("=" * 70)
        print("📋 REPORTE FINAL DE EVALUACIÓN DEL MODELO")
        print("=" * 70 + "\n")
        
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "evaluation_sections": list(self.results.keys()),
            "key_metrics": {
                "inference_speed_texts_per_second": 
                    self.results.get("inference_speed", {}).get("texts_per_second", 0),
                "similarity_accuracy": 
                    self.results.get("similarity_metrics", {}).get("accuracy_on_test_pairs", 0),
                "search_mrr": 
                    self.results.get("search_quality", {}).get("mrr", 0),
                "search_ndcg": 
                    self.results.get("search_quality", {}).get("ndcg", 0),
                "clustering_cohesion": 
                    self.results.get("clustering_quality", {}).get("average_cohesion", 0),
            }
        }
        
        print("📊 MÉTRICAS PRINCIPALES:")
        print(f"  • Velocidad: {summary['key_metrics']['inference_speed_texts_per_second']:.0f} textos/seg")
        print(f"  • Precisión similitud: {summary['key_metrics']['similarity_accuracy']*100:.1f}%")
        print(f"  • MRR (búsqueda): {summary['key_metrics']['search_mrr']:.4f}")
        print(f"  • NDCG (búsqueda): {summary['key_metrics']['search_ndcg']:.4f}")
        print(f"  • Cohesión clustering: {summary['key_metrics']['clustering_cohesion']:.4f}")
        print("\n✅ Evaluación completada exitosamente")
        
        return summary
    
    # =========================================================================
    # 8. GUARDAR RESULTADOS
    # =========================================================================
    
    def save_results(self, output_path: str = "evaluation_results.json"):
        """Guardar resultados en JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"💾 Resultados guardados en: {output_path}")
    
    def run_full_evaluation(self):
        """Ejecutar evaluación completa"""
        print("\n" + "=" * 70)
        print("🚀 INICIANDO EVALUACIÓN COMPLETA DEL MODELO")
        print("=" * 70 + "\n")
        
        # Ejecutar todas las evaluaciones
        self.measure_inference_speed(num_texts=100)
        self.measure_similarity_metrics()
        self.measure_search_quality()
        self.measure_clustering_quality()
        self.measure_embedding_distribution()
        self.measure_multilingual_performance()
        
        # Resumen
        summary = self.generate_summary_report()
        
        # Guardar
        self.save_results()
        
        print("\n" + "=" * 70)
        
        return self.results


# =========================================================================
# SCRIPT PRINCIPAL
# =========================================================================

if __name__ == "__main__":
    import sys
    
    # Detectar ruta del modelo
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    else:
        model_path = "./model"
    
    # Crear evaluador
    evaluator = ModelEvaluator(model_path, device="cpu")
    
    # Ejecutar evaluación completa
    results = evaluator.run_full_evaluation()
