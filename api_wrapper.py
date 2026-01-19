"""
API WRAPPER - Usar el modelo como servicio REST
Permite acceder al modelo desde cualquier aplicación
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional
import numpy as np

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn

from loader import load_model


# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class EmbedRequest(BaseModel):
    """Solicitud de embedding"""
    texts: List[str]
    device: Optional[str] = "cpu"


class EmbedResponse(BaseModel):
    """Respuesta de embedding"""
    embeddings: List[List[float]]
    dimension: int
    count: int


class SimilarityRequest(BaseModel):
    """Solicitud de similitud"""
    text1: str
    text2: str


class SimilarityResponse(BaseModel):
    """Respuesta de similitud"""
    text1: str
    text2: str
    similarity: float


class SearchRequest(BaseModel):
    """Solicitud de búsqueda"""
    query: str
    candidates: List[str]
    top_k: Optional[int] = None


class SearchResult(BaseModel):
    """Resultado individual de búsqueda"""
    candidate: str
    similarity: float
    rank: int


class SearchResponse(BaseModel):
    """Respuesta de búsqueda"""
    query: str
    total_results: int
    results: List[SearchResult]


class ClusterRequest(BaseModel):
    """Solicitud de clustering"""
    texts: List[str]
    n_clusters: int = 3


class ClusterResponse(BaseModel):
    """Respuesta de clustering"""
    n_clusters: int
    total_texts: int
    clusters: dict


class InfoResponse(BaseModel):
    """Información del modelo"""
    device: str
    embedding_dimension: int
    model_type: str
    base_model: str
    training: Optional[dict] = None


# ============================================================================
# APLICACIÓN FASTAPI
# ============================================================================

app = FastAPI(
    title="Modelo Entrenado - API",
    description="API para acceder al modelo de embeddings entrenado",
    version="1.0.0"
)

# Variable global para el modelo
MODEL = None


def initialize_model(model_path: str, device: str = "cpu"):
    """Inicializar el modelo"""
    global MODEL
    MODEL = load_model(model_path, device=device)
    print(f"✅ Modelo inicializado: {model_path}")


@app.on_event("startup")
async def startup_event():
    """Evento de startup"""
    if MODEL is None:
        raise RuntimeError("Modelo no inicializado. Use initialize_model() primero.")
    print("🚀 API iniciada")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de shutdown"""
    print("👋 API cerrada")


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API del Modelo Entrenado",
        "version": "1.0.0",
        "endpoints": [
            "/embed - Generar embeddings",
            "/similarity - Calcular similitud",
            "/search - Buscar candidatos",
            "/cluster - Agrupar textos",
            "/info - Información del modelo",
            "/docs - Documentación Swagger"
        ]
    }


@app.get("/info", tags=["Info"], response_model=InfoResponse)
async def get_info():
    """Obtener información del modelo"""
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    return MODEL.get_info()


@app.post("/embed", tags=["Embeddings"], response_model=EmbedResponse)
async def embed(request: EmbedRequest):
    """
    Generar embeddings para textos
    
    Parámetros:
    - texts: Lista de textos
    
    Retorna:
    - embeddings: Lista de vectores (768 dimensiones cada uno)
    - dimension: Dimensiones de los embeddings
    - count: Número de embeddings generados
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    if not request.texts:
        raise HTTPException(status_code=400, detail="Lista de textos vacía")
    
    try:
        embeddings = MODEL.encode(request.texts)
        
        # Asegurar que es una lista de listas
        if isinstance(embeddings, np.ndarray):
            if len(embeddings.shape) == 1:
                embeddings = [embeddings.tolist()]
            else:
                embeddings = embeddings.tolist()
        
        return EmbedResponse(
            embeddings=embeddings,
            dimension=768,
            count=len(embeddings)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/similarity", tags=["Similitud"], response_model=SimilarityResponse)
async def similarity(request: SimilarityRequest):
    """
    Calcular similitud entre dos textos
    
    Parámetros:
    - text1: Primer texto
    - text2: Segundo texto
    
    Retorna:
    - similarity: Valor de similitud (0-1)
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    if not request.text1 or not request.text2:
        raise HTTPException(status_code=400, detail="Textos vacíos")
    
    try:
        sim = MODEL.similarity(request.text1, request.text2)
        
        return SimilarityResponse(
            text1=request.text1,
            text2=request.text2,
            similarity=sim
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/search", tags=["Búsqueda"], response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Buscar candidatos similares a una consulta
    
    Parámetros:
    - query: Texto de búsqueda
    - candidates: Lista de candidatos
    - top_k: Número de resultados (opcional)
    
    Retorna:
    - results: Lista de candidatos ordenados por similitud
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    if not request.query or not request.candidates:
        raise HTTPException(status_code=400, detail="Query o candidatos vacíos")
    
    try:
        results = MODEL.search(request.query, request.candidates, request.top_k)
        
        search_results = [
            SearchResult(
                candidate=r["candidate"],
                similarity=r["similarity"],
                rank=i + 1
            )
            for i, r in enumerate(results)
        ]
        
        return SearchResponse(
            query=request.query,
            total_results=len(search_results),
            results=search_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/cluster", tags=["Clustering"], response_model=ClusterResponse)
async def cluster(request: ClusterRequest):
    """
    Agrupar textos en clusters
    
    Parámetros:
    - texts: Lista de textos
    - n_clusters: Número de clusters
    
    Retorna:
    - clusters: Diccionario con textos agrupados
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    if not request.texts:
        raise HTTPException(status_code=400, detail="Lista de textos vacía")
    
    try:
        clusters = MODEL.cluster(request.texts, request.n_clusters)
        
        return ClusterResponse(
            n_clusters=request.n_clusters,
            total_texts=len(request.texts),
            clusters=clusters
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "model_loaded": MODEL is not None
    }


# ============================================================================
# EJEMPLOS DE CLIENTE
# ============================================================================

EJEMPLOS_CLIENTE = """
# EJEMPLOS DE USO DE LA API

## 1. Generar Embeddings
curl -X POST http://localhost:8000/embed \\
  -H "Content-Type: application/json" \\
  -d '{
    "texts": ["python developer", "java engineer"]
  }'

## 2. Calcular Similitud
curl -X POST http://localhost:8000/similarity \\
  -H "Content-Type: application/json" \\
  -d '{
    "text1": "python developer",
    "text2": "python engineer"
  }'

## 3. Buscar Candidatos
curl -X POST http://localhost:8000/search \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "python senior developer",
    "candidates": [
      "java programmer",
      "python engineer",
      "fullstack javascript",
      "python specialist"
    ],
    "top_k": 2
  }'

## 4. Agrupar Textos
curl -X POST http://localhost:8000/cluster \\
  -H "Content-Type: application/json" \\
  -d '{
    "texts": [
      "python developer",
      "python engineer",
      "java developer",
      "java programmer",
      "frontend react"
    ],
    "n_clusters": 3
  }'

## 5. Información del Modelo
curl http://localhost:8000/info

## 6. Health Check
curl http://localhost:8000/health
"""


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="API para el modelo entrenado",
        epilog=EJEMPLOS_CLIENTE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--model-path",
        type=str,
        default="./model",
        help="Ruta al directorio del modelo (default: ./model)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Puerto de escucha (default: 8000)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host de escucha (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--device",
        type=str,
        choices=["cpu", "cuda"],
        default="cpu",
        help="Dispositivo a usar (default: cpu)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Reload automático en desarrollo"
    )
    
    args = parser.parse_args()
    
    # Validar que existe el modelo
    model_path = Path(args.model_path)
    if not (model_path / "model.safetensors").exists() and \
       not (model_path / "model" / "model.safetensors").exists():
        print(f"❌ Error: Modelo no encontrado en {args.model_path}")
        sys.exit(1)
    
    # Inicializar modelo
    print(f"\n📦 Inicializando modelo desde: {args.model_path}")
    initialize_model(str(model_path), device=args.device)
    
    # Iniciar servidor
    print(f"\n🚀 Iniciando API en http://{args.host}:{args.port}")
    print(f"📖 Documentación: http://{args.host}:{args.port}/docs")
    print(f"🔧 Health check: http://{args.host}:{args.port}/health\n")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
