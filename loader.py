"""
LOADER UNIVERSAL PARA MODELO ENTRENADO
Permite cargar el modelo desde cualquier proyecto
"""

import os
import json
from pathlib import Path
from typing import Optional, Union, List
import numpy as np
from sentence_transformers import SentenceTransformer


class ModeloPortable:
    """Wrapper universal para el modelo entrenado"""
    
    def __init__(self, model_path: str, device: str = "cpu"):
        """
        Inicializar modelo
        
        Args:
            model_path: Ruta al directorio del modelo o ruta directa a archivos
            device: 'cpu' o 'cuda'
        """
        self.device = device
        self.model_path = Path(model_path)
        
        # Buscar directorio del modelo
        if (self.model_path / "model.safetensors").exists():
            # Ya está en la carpeta correcta
            actual_path = str(self.model_path)
        elif (self.model_path / "model" / "model.safetensors").exists():
            # Está en subdirectorio model/
            actual_path = str(self.model_path / "model")
        else:
            raise FileNotFoundError(f"No se encontró modelo en {model_path}")
        
        print(f"📦 Cargando modelo desde: {actual_path}")
        self.model = SentenceTransformer(actual_path, device=device)
        
        # Cargar metadata si existe
        self.metadata = self._load_metadata(actual_path)
        print(f"✅ Modelo cargado correctamente (Device: {device})")
    
    def _load_metadata(self, model_path: str) -> dict:
        """Cargar metadata del modelo"""
        metadata_path = Path(model_path) / "training_metadata.json"
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return {}
    
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generar embeddings para textos
        
        Args:
            texts: Texto o lista de textos
        
        Returns:
            numpy array con embeddings (768 dimensiones)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(texts)
        
        if len(texts) == 1:
            return embeddings[0]
        return embeddings
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calcular similitud entre dos textos
        
        Args:
            text1: Primer texto
            text2: Segundo texto
        
        Returns:
            Similitud (0-1)
        """
        from sklearn.metrics.pairwise import cosine_similarity
        
        emb1 = self.encode(text1)
        emb2 = self.encode(text2)
        
        sim = cosine_similarity([emb1], [emb2])[0][0]
        return float(sim)
    
    def search(self, query: str, candidates: List[str], top_k: int = None) -> List[dict]:
        """
        Buscar candidatos similares a una consulta
        
        Args:
            query: Texto de búsqueda
            candidates: Lista de candidatos
            top_k: Número de resultados (None = todos)
        
        Returns:
            Lista de resultados ordenados por similitud
        """
        from sklearn.metrics.pairwise import cosine_similarity
        
        query_emb = self.encode(query)
        candidates_emb = np.array([self.encode(c) for c in candidates])
        
        # Calcular similitudes
        similarities = cosine_similarity([query_emb], candidates_emb)[0]
        
        # Crear resultados
        results = []
        for candidate, similarity in zip(candidates, similarities):
            results.append({
                "candidate": candidate,
                "similarity": float(similarity),
                "score": float(similarity)
            })
        
        # Ordenar por similitud descendente
        results = sorted(results, key=lambda x: x["similarity"], reverse=True)
        
        # Limitar a top_k si se especifica
        if top_k:
            results = results[:top_k]
        
        return results
    
    def cluster(self, texts: List[str], n_clusters: int = 3) -> dict:
        """
        Agrupar textos en clusters
        
        Args:
            texts: Lista de textos
            n_clusters: Número de clusters
        
        Returns:
            Diccionario con clusters
        """
        from sklearn.cluster import KMeans
        
        # Generar embeddings
        embeddings = np.array([self.encode(text) for text in texts])
        
        # Clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings)
        
        # Agrupar
        clusters = {i: [] for i in range(n_clusters)}
        for text, label in zip(texts, labels):
            clusters[label].append(text)
        
        return clusters
    
    def get_info(self) -> dict:
        """Obtener información del modelo"""
        info = {
            "device": self.device,
            "embedding_dimension": 768,
            "model_type": "sentence-transformers",
            "base_model": "paraphrase-multilingual-mpnet-base-v2",
        }
        
        if self.metadata:
            info["training"] = self.metadata.get("training_config", {})
            info["timestamp"] = self.metadata.get("timestamp", "Unknown")
        
        return info


def load_model(model_path: str, device: str = "cpu") -> ModeloPortable:
    """
    Función auxiliar para cargar modelo
    
    Args:
        model_path: Ruta al modelo
        device: 'cpu' o 'cuda'
    
    Returns:
        Instancia de ModeloPortable
    """
    return ModeloPortable(model_path, device=device)


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Usar: python loader.py <ruta_modelo> [test|info]
    
    if len(sys.argv) < 2:
        print("""
Uso: python loader.py <ruta_modelo> [comando]

Comandos:
  test    - Probar el modelo con ejemplos
  info    - Mostrar información del modelo
  
Ejemplos:
  python loader.py ./modelo_entrenado_multiloss_portable test
  python loader.py ./modelo_entrenado_multiloss_portable info
        """)
        sys.exit(1)
    
    model_path = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "test"
    
    # Cargar modelo
    modelo = load_model(model_path)
    
    if command == "test":
        print("\n" + "="*70)
        print("TEST DEL MODELO")
        print("="*70)
        
        # Test 1: Embedding simple
        print("\n1. Generar embedding:")
        text = "desarrollador python senior"
        embedding = modelo.encode(text)
        print(f"   Texto: '{text}'")
        print(f"   Dimensiones: {embedding.shape}")
        print(f"   Primeros 5 valores: {embedding[:5]}")
        
        # Test 2: Similitud
        print("\n2. Calcular similitud:")
        text1 = "python developer"
        text2 = "python engineer"
        sim = modelo.similarity(text1, text2)
        print(f"   '{text1}' vs '{text2}'")
        print(f"   Similitud: {sim:.4f}")
        
        # Test 3: Búsqueda
        print("\n3. Búsqueda:")
        query = "python developer"
        candidates = [
            "java programmer",
            "python engineer",
            "fullstack javascript",
            "python specialist"
        ]
        results = modelo.search(query, candidates)
        print(f"   Búsqueda: '{query}'")
        for r in results:
            print(f"     {r['similarity']:.4f} - {r['candidate']}")
        
        # Test 4: Información
        print("\n4. Información del modelo:")
        info = modelo.get_info()
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        print("\n✅ TESTS COMPLETADOS\n")
    
    elif command == "info":
        print("\n" + "="*70)
        print("INFORMACIÓN DEL MODELO")
        print("="*70)
        
        info = modelo.get_info()
        for key, value in info.items():
            print(f"{key:20}: {value}")
        
        print("\n" + "="*70 + "\n")
