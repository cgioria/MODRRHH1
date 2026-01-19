"""
API REST PARA EL AGENTE DE RECRUITMENT
Usando FastAPI para crear endpoints que exponen el agente

Para ejecutar:
    uvicorn agent_api:app --reload --port 8000

Luego acceder a:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from .agents_advanced import AdvancedRecruitmentAgent


# =========================================================================
# PYDANTIC MODELS (Esquemas)
# =========================================================================

class QueryRequest(BaseModel):
    """Request para procesar una query"""
    text: str


class SearchRequest(BaseModel):
    """Request para búsqueda"""
    query: str
    top_k: int = 5


class MatchingRequest(BaseModel):
    """Request para matching"""
    candidate_id: str
    job_id: str


class MatchScore(BaseModel):
    """Score de matching"""
    candidate_name: str
    job_title: str
    profile_similarity: float
    skills_match: float
    experience_match: float
    overall_score: float
    recommendation: str


class CandidateResponse(BaseModel):
    """Response de candidato"""
    id: str
    name: str
    profile: str
    skills: List[str]
    years: int
    location: str
    match_score: Optional[float] = None


class JobResponse(BaseModel):
    """Response de posición"""
    id: str
    title: str
    description: str
    required_skills: List[str]
    years_required: int
    salary_range: str
    match_score: Optional[float] = None


# =========================================================================
# INICIALIZAR APP Y AGENTE
# =========================================================================

app = FastAPI(
    title="🤖 Recruitment Agent API",
    description="API REST para agente de recruitment con embeddings",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar agente
agent = AdvancedRecruitmentAgent("./model")


# =========================================================================
# ENDPOINTS: INFORMACIÓN
# =========================================================================

@app.get("/health")
async def health_check():
    """Health check - verifica que el servicio está disponible"""
    return {
        "status": "healthy",
        "agent": "active",
        "model": "paraphrase-multilingual-mpnet-base-v2",
        "candidates": len(agent.candidates_db),
        "jobs": len(agent.jobs_db)
    }


@app.get("/info")
async def get_info():
    """Información del agente y base de datos"""
    return {
        "agent": "Advanced Recruitment Agent",
        "version": "1.0.0",
        "model": {
            "name": "paraphrase-multilingual-mpnet-base-v2",
            "dimension": 768,
            "performance": {
                "search_mrr": 1.0,
                "search_ndcg": 0.993,
                "multilingual": True
            }
        },
        "database": {
            "candidates": len(agent.candidates_db),
            "jobs": len(agent.jobs_db),
            "operations": ["search", "match", "recommend", "cluster"]
        }
    }


# =========================================================================
# ENDPOINTS: CANDIDATOS
# =========================================================================

@app.get("/candidates")
async def list_candidates() -> List[CandidateResponse]:
    """Listar todos los candidatos"""
    return [CandidateResponse(**c) for c in agent.candidates_db]


@app.get("/candidates/{candidate_id}")
async def get_candidate(candidate_id: str) -> CandidateResponse:
    """Obtener detalles de un candidato específico"""
    candidate = next((c for c in agent.candidates_db if c["id"] == candidate_id), None)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return CandidateResponse(**candidate)


@app.post("/candidates/search")
async def search_candidates(request: SearchRequest) -> List[CandidateResponse]:
    """
    Buscar candidatos por similitud
    
    Ejemplo:
    {
        "query": "Senior Python Developer with Machine Learning",
        "top_k": 5
    }
    """
    try:
        results = agent.search_candidates(request.query, top_k=request.top_k)
        return [CandidateResponse(**c) for c in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# ENDPOINTS: POSICIONES
# =========================================================================

@app.get("/jobs")
async def list_jobs() -> List[JobResponse]:
    """Listar todas las posiciones disponibles"""
    return [JobResponse(**j) for j in agent.jobs_db]


@app.get("/jobs/{job_id}")
async def get_job(job_id: str) -> JobResponse:
    """Obtener detalles de una posición específica"""
    job = next((j for j in agent.jobs_db if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Posición no encontrada")
    return JobResponse(**job)


# =========================================================================
# ENDPOINTS: MATCHING
# =========================================================================

@app.post("/match")
async def calculate_match(request: MatchingRequest) -> Dict:
    """
    Calcular matching entre candidato y posición
    
    Retorna: scores de similitud, skill match, experience match, etc.
    
    Ejemplo:
    {
        "candidate_id": "C001",
        "job_id": "J001"
    }
    """
    try:
        result = agent.calculate_candidate_job_match(
            request.candidate_id,
            request.job_id
        )
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs/{job_id}/top-candidates")
async def get_top_candidates_for_job(
    job_id: str,
    top_k: int = 5
) -> List[Dict]:
    """
    Obtener top-k candidatos para una posición
    
    Retorna candidatos rankeados por score de matching
    """
    try:
        results = agent.get_top_candidates_for_job(job_id, top_k=top_k)
        if not results:
            raise HTTPException(status_code=404, detail="Posición no encontrada")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/candidates/{candidate_id}/recommended-jobs")
async def get_recommended_jobs(
    candidate_id: str,
    top_k: int = 3
) -> List[Dict]:
    """
    Obtener recomendaciones de posiciones para un candidato
    
    Retorna posiciones rankeadas por relevancia
    """
    try:
        results = agent.get_job_recommendations_for_candidate(candidate_id, top_k=top_k)
        if not results:
            raise HTTPException(status_code=404, detail="Candidato no encontrado")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# ENDPOINTS: AGENTE CONVERSACIONAL
# =========================================================================

@app.post("/query")
async def process_query(request: QueryRequest) -> Dict:
    """
    Procesar una query conversacional
    
    El agente entiende diferentes intents y ejecuta las herramientas apropiadas
    
    Ejemplos de queries:
    - "Busca desarrolladores Python senior"
    - "Match Alice Johnson con Senior Backend Python Developer"
    - "Recomienda posiciones para David Lee"
    - "Top candidatos para Frontend React Developer"
    """
    try:
        response = agent.process_user_input(request.text)
        return {
            "query": request.text,
            "response": response,
            "timestamp": agent.conversation_history[-1]["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation-history")
async def get_conversation_history() -> List[Dict]:
    """Obtener historial de conversación"""
    return agent.conversation_history


# =========================================================================
# ENDPOINTS: BATCH OPERATIONS
# =========================================================================

@app.post("/batch/match-all")
async def batch_match_all_candidates_to_job(job_id: str) -> List[Dict]:
    """
    Calcular matching de TODOS los candidatos con una posición
    
    Retorna ranking completo (útil para screening)
    """
    try:
        results = []
        for candidate in agent.candidates_db:
            match_data = agent.calculate_candidate_job_match(candidate["id"], job_id)
            if "error" not in match_data:
                results.append(match_data)
        
        # Ordenar por score
        results.sort(key=lambda x: x["overall_score"], reverse=True)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch/screen-cv")
async def screen_new_cv(profile: str) -> Dict:
    """
    Hacer screening automático de un CV nuevo
    
    Busca las mejores posiciones para el CV
    """
    try:
        # Buscar posiciones más relevantes
        job_texts = [j["description"] for j in agent.jobs_db]
        results = agent.model.search(profile, job_texts, top_k=len(agent.jobs_db))
        
        recommendations = []
        for result in results:
            for i, jtext in enumerate(job_texts):
                if jtext == result["candidate"]:
                    job = agent.jobs_db[i]
                    recommendations.append({
                        "job_title": job["title"],
                        "job_id": job["id"],
                        "match_score": float(result["similarity"]),
                        "recommendation": agent._get_recommendation(result["similarity"])
                    })
                    break
        
        return {
            "cv_profile": profile,
            "recommendations": recommendations,
            "best_fit": recommendations[0] if recommendations else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# ENDPOINTS: ANÁLISIS
# =========================================================================

@app.get("/analytics/candidates-by-skills")
async def candidates_by_skills() -> Dict[str, List[str]]:
    """Agrupar candidatos por skills"""
    skills_map = {}
    for candidate in agent.candidates_db:
        for skill in candidate["skills"]:
            if skill not in skills_map:
                skills_map[skill] = []
            skills_map[skill].append(candidate["name"])
    return skills_map


@app.get("/analytics/jobs-by-skills")
async def jobs_by_skills() -> Dict[str, List[str]]:
    """Agrupar posiciones por skills requeridos"""
    skills_map = {}
    for job in agent.jobs_db:
        for skill in job["required_skills"]:
            if skill not in skills_map:
                skills_map[skill] = []
            skills_map[skill].append(job["title"])
    return skills_map


# =========================================================================
# ERROR HANDLERS
# =========================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


# =========================================================================
# ROOT
# =========================================================================

@app.get("/")
async def root():
    """Root endpoint - información de bienvenida"""
    return {
        "message": "🤖 Welcome to Recruitment Agent API",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
        "endpoints": {
            "info": "/info",
            "health": "/health",
            "candidates": "/candidates",
            "jobs": "/jobs",
            "search": "/candidates/search (POST)",
            "match": "/match (POST)",
            "query": "/query (POST)",
            "recommendations": "/candidates/{id}/recommended-jobs",
            "top_candidates": "/jobs/{id}/top-candidates"
        }
    }


# =========================================================================
# SI SE EJECUTA DIRECTAMENTE
# =========================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


"""
EJEMPLOS DE USO CON CURL
═════════════════════════════════════════════════════════════════

1. Health Check:
   curl http://localhost:8000/health

2. Listar Candidatos:
   curl http://localhost:8000/candidates

3. Buscar Candidatos:
   curl -X POST http://localhost:8000/candidates/search \\
     -H "Content-Type: application/json" \\
     -d '{"query": "Python Developer", "top_k": 5}'

4. Matching:
   curl -X POST http://localhost:8000/match \\
     -H "Content-Type: application/json" \\
     -d '{"candidate_id": "C001", "job_id": "J001"}'

5. Top Candidatos para Job:
   curl http://localhost:8000/jobs/J001/top-candidates?top_k=5

6. Recomendaciones para Candidato:
   curl http://localhost:8000/candidates/C001/recommended-jobs?top_k=3

7. Procesar Query (Conversacional):
   curl -X POST http://localhost:8000/query \\
     -H "Content-Type: application/json" \\
     -d '{"text": "Busca desarrolladores Python senior"}'

═════════════════════════════════════════════════════════════════

USO CON PYTHON REQUESTS
════════════════════════════════════════════════════════════════

import requests

BASE_URL = "http://localhost:8000"

# Buscar candidatos
response = requests.post(
    f"{BASE_URL}/candidates/search",
    json={"query": "Python Developer", "top_k": 5}
)
print(response.json())

# Calcular matching
response = requests.post(
    f"{BASE_URL}/match",
    json={"candidate_id": "C001", "job_id": "J001"}
)
print(response.json())

# Query conversacional
response = requests.post(
    f"{BASE_URL}/query",
    json={"text": "Recomienda posiciones para Alice Johnson"}
)
print(response.json())

════════════════════════════════════════════════════════════════
"""
