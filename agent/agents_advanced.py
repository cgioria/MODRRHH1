"""
AGENTE AVANZADO CON LANGCHAIN Y LLM
Nivel: Intermediate/Advanced
Complejidad: Alta
Dependencias: langchain, openai (o alternative LLM)

Este agente combina:
  • Tu modelo para búsqueda y matching
  • LLM (OpenAI/Claude) para entendimiento del lenguaje
  • Memory para contexto en conversaciones
  • Tools para operaciones específicas
"""

from typing import List, Dict, Optional, Tuple
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loader import load_model
import json
from datetime import datetime


class AdvancedRecruitmentAgent:
    """
    Agente avanzado para recruitment con LangChain
    
    Este es un template que muestra cómo integrar:
    - Tu modelo como herramienta principal
    - LLM para procesamiento de lenguaje natural
    - Memory para contexto
    - State management
    """
    
    def __init__(self, model_path: str = None):
        """Inicializar agente avanzado"""
        if model_path is None:
            # Usar ruta relativa al proyecto raíz
            project_root = Path(__file__).parent.parent
            model_path = str(project_root / "model")
        
        self.model = load_model(model_path)
        
        # Estado del agente
        self.conversation_history: List[Dict] = []
        self.current_context: Dict = {}
        self.search_cache: Dict = {}
        
        # Base de datos de candidatos (en producción: PostgreSQL)
        self.candidates_db = self._load_candidates_db()
        self.jobs_db = self._load_jobs_db()
        
        # Embeddings pre-calculados para speedup
        self.candidate_embeddings = None
        self.job_embeddings = None
        
        print("✅ Agente Avanzado inicializado")
        print(f"   Modelo: {model_path}")
        print(f"   Candidatos: {len(self.candidates_db)}")
        print(f"   Posiciones: {len(self.jobs_db)}")
    
    # =========================================================================
    # CARGA DE DATOS
    # =========================================================================
    
    def _load_candidates_db(self) -> List[Dict]:
        """Cargar base de datos de candidatos"""
        return [
            {
                "id": "C001",
                "name": "Alice Johnson",
                "profile": "Senior Python Developer with 10 years experience",
                "skills": ["Python", "Django", "Machine Learning"],
                "years": 10,
                "location": "San Francisco"
            },
            {
                "id": "C002",
                "name": "Bob Smith",
                "profile": "Python backend engineer specializing in APIs",
                "skills": ["Python", "FastAPI", "PostgreSQL"],
                "years": 6,
                "location": "New York"
            },
            {
                "id": "C003",
                "name": "Carol Davis",
                "profile": "Frontend Developer expert in React and Vue",
                "skills": ["React", "Vue", "TypeScript"],
                "years": 5,
                "location": "Austin"
            },
            {
                "id": "C004",
                "name": "David Lee",
                "profile": "Data Scientist specialized in Machine Learning",
                "skills": ["Python", "ML", "TensorFlow"],
                "years": 8,
                "location": "Boston"
            },
        ]
    
    def _load_jobs_db(self) -> List[Dict]:
        """Cargar base de datos de posiciones"""
        return [
            {
                "id": "J001",
                "title": "Senior Backend Python Developer",
                "description": "We are looking for a senior backend developer with python expertise",
                "required_skills": ["Python", "Backend", "APIs"],
                "years_required": 5,
                "salary_range": "$120k-$150k"
            },
            {
                "id": "J002",
                "title": "Frontend React Developer",
                "description": "Frontend developer needed for react-based web application",
                "required_skills": ["React", "JavaScript", "CSS"],
                "years_required": 3,
                "salary_range": "$100k-$130k"
            },
            {
                "id": "J003",
                "title": "Machine Learning Engineer",
                "description": "ML engineer to build and deploy machine learning models",
                "required_skills": ["Python", "ML", "Deep Learning"],
                "years_required": 5,
                "salary_range": "$130k-$160k"
            },
        ]
    
    # =========================================================================
    # HERRAMIENTAS: BÚSQUEDA
    # =========================================================================
    
    def search_candidates(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Buscar candidatos por similaridad
        
        Herramienta 1: Búsqueda de candidatos
        """
        # Convertir candidatos a textos para búsqueda
        candidate_texts = [c["profile"] for c in self.candidates_db]
        
        # Usar modelo para búsqueda
        results = self.model.search(query, candidate_texts, top_k=top_k)
        
        # Mapear resultados a candidatos completos
        matched_candidates = []
        for result in results:
            # Encontrar el candidato correspondiente
            for i, ctext in enumerate(candidate_texts):
                if ctext == result["candidate"]:
                    candidate = self.candidates_db[i].copy()
                    candidate["match_score"] = result["similarity"]
                    matched_candidates.append(candidate)
                    break
        
        # Caché para siguiente búsqueda similar
        self.search_cache[query] = matched_candidates
        
        return matched_candidates
    
    def search_jobs(self, candidate_profile: str, top_k: int = 3) -> List[Dict]:
        """
        Buscar posiciones apropiadas para un candidato
        
        Herramienta 2: Búsqueda de posiciones
        """
        job_texts = [j["description"] for j in self.jobs_db]
        
        results = self.model.search(candidate_profile, job_texts, top_k=top_k)
        
        matched_jobs = []
        for result in results:
            for i, jtext in enumerate(job_texts):
                if jtext == result["candidate"]:
                    job = self.jobs_db[i].copy()
                    job["match_score"] = result["similarity"]
                    matched_jobs.append(job)
                    break
        
        return matched_jobs
    
    # =========================================================================
    # HERRAMIENTAS: MATCHING Y SCORING
    # =========================================================================
    
    def calculate_candidate_job_match(
        self, 
        candidate_id: str, 
        job_id: str
    ) -> Dict:
        """
        Calcular match score entre candidato y posición
        
        Herramienta 3: Matching detallado
        """
        # Encontrar candidato y job
        candidate = next((c for c in self.candidates_db if c["id"] == candidate_id), None)
        job = next((j for j in self.jobs_db if j["id"] == job_id), None)
        
        if not candidate or not job:
            return {"error": "Candidato o posición no encontrados"}
        
        # Calcular similitud de perfiles
        profile_similarity = self.model.similarity(
            candidate["profile"],
            job["description"]
        )
        
        # Calcular skills match
        skills_match = len(set(candidate["skills"]) & set(job["required_skills"])) / len(job["required_skills"])
        
        # Calcular experience match
        experience_match = 1.0 if candidate["years"] >= job["years_required"] else candidate["years"] / job["years_required"]
        
        # Score combinado
        overall_score = (profile_similarity * 0.5 + skills_match * 0.3 + experience_match * 0.2)
        
        return {
            "candidate": candidate,
            "job": job,
            "profile_similarity": float(profile_similarity),
            "skills_match": float(skills_match),
            "experience_match": float(experience_match),
            "overall_score": float(overall_score),
            "recommendation": self._get_recommendation(overall_score),
            "details": self._get_match_details(candidate, job)
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Obtener recomendación basada en score"""
        if score >= 0.8:
            return "🟢 EXCELENTE MATCH - Proceder con entrevista"
        elif score >= 0.6:
            return "🟡 BUEN MATCH - Considerar para entrevista"
        elif score >= 0.4:
            return "🟠 MATCH MODERADO - Revisar con HR"
        else:
            return "🔴 BAJO MATCH - No recomendado por ahora"
    
    def _get_match_details(self, candidate: Dict, job: Dict) -> str:
        """Generar descripción detallada del match"""
        details = f"""
Candidato: {candidate['name']}
Perfil: {candidate['profile']}
Skills: {', '.join(candidate['skills'])}
Experiencia: {candidate['years']} años

Posición: {job['title']}
Descripción: {job['description']}
Skills requeridos: {', '.join(job['required_skills'])}
Experiencia requerida: {job['years_required']} años
"""
        return details.strip()
    
    # =========================================================================
    # HERRAMIENTAS: ANÁLISIS Y RECOMENDACIONES
    # =========================================================================
    
    def get_top_candidates_for_job(self, job_id: str, top_k: int = 5) -> List[Dict]:
        """
        Obtener top-k candidatos para una posición
        
        Herramienta 4: Análisis de posición
        """
        job = next((j for j in self.jobs_db if j["id"] == job_id), None)
        if not job:
            return []
        
        # Buscar candidatos similares
        candidates = self.search_candidates(job["description"], top_k=len(self.candidates_db))
        
        # Calcular scores completos
        results = []
        for candidate in candidates[:top_k]:
            match_data = self.calculate_candidate_job_match(candidate["id"], job_id)
            results.append(match_data)
        
        # Ordenar por score
        results.sort(key=lambda x: x["overall_score"], reverse=True)
        
        return results
    
    def get_job_recommendations_for_candidate(self, candidate_id: str, top_k: int = 3) -> List[Dict]:
        """
        Obtener recomendaciones de posiciones para un candidato
        
        Herramienta 5: Recomendaciones personalizadas
        """
        candidate = next((c for c in self.candidates_db if c["id"] == candidate_id), None)
        if not candidate:
            return []
        
        # Buscar posiciones similares
        jobs = self.search_jobs(candidate["profile"], top_k=len(self.jobs_db))
        
        # Calcular scores
        results = []
        for job in jobs[:top_k]:
            match_data = self.calculate_candidate_job_match(candidate_id, job["id"])
            results.append(match_data)
        
        # Ordenar por score
        results.sort(key=lambda x: x["overall_score"], reverse=True)
        
        return results
    
    # =========================================================================
    # PROCESAMIENTO CONVERSACIONAL
    # =========================================================================
    
    def process_user_input(self, user_input: str) -> str:
        """
        Procesar input del usuario y retornar respuesta
        
        En una implementación real con LangChain:
        1. Se usaría un LLM para entender la intent
        2. Se seleccionarían automáticamente las herramientas
        3. Se ejecutarían y se formatearía la respuesta
        
        Para este ejemplo, usamos reglas simples
        """
        
        # Agregar a historial
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "type": "user"
        })
        
        # Detectar intent y ejecutar herramienta correspondiente
        user_lower = user_input.lower()
        
        if "busca" in user_lower or "search" in user_lower:
            response = self._handle_search_request(user_input)
        
        elif "match" in user_lower:
            response = self._handle_matching_request(user_input)
        
        elif "recomienda" in user_lower or "recommend" in user_lower:
            response = self._handle_recommendation_request(user_input)
        
        elif "candidatos" in user_lower and ("para" in user_lower or "for" in user_lower):
            response = self._handle_candidates_for_job(user_input)
        
        else:
            response = self._show_help()
        
        # Agregar respuesta al historial
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "assistant": response,
            "type": "assistant"
        })
        
        return response
    
    def _handle_search_request(self, user_input: str) -> str:
        """Manejar request de búsqueda"""
        results = self.search_candidates(user_input, top_k=5)
        
        if not results:
            return "❌ No encontré candidatos relevantes"
        
        response = "🔎 CANDIDATOS ENCONTRADOS:\n\n"
        for i, candidate in enumerate(results, 1):
            response += f"{i}. {candidate['name']}\n"
            response += f"   Perfil: {candidate['profile']}\n"
            response += f"   Match: {candidate['match_score']:.1%}\n"
            response += f"   Skills: {', '.join(candidate['skills'])}\n\n"
        
        return response
    
    def _handle_matching_request(self, user_input: str) -> str:
        """Manejar request de matching"""
        
        # Buscar IDs mencionados
        candidate_id = None
        job_id = None
        
        for c in self.candidates_db:
            if c["name"].lower() in user_input.lower():
                candidate_id = c["id"]
                break
        
        for j in self.jobs_db:
            if j["title"].lower() in user_input.lower():
                job_id = j["id"]
                break
        
        if not candidate_id or not job_id:
            return "❌ No especificaste candidato y posición claramente"
        
        match_data = self.calculate_candidate_job_match(candidate_id, job_id)
        
        response = f"""
📊 ANÁLISIS DE MATCHING
═══════════════════════════════════════════

Candidato: {match_data['candidate']['name']}
Posición: {match_data['job']['title']}

SCORES:
  • Similitud de perfil: {match_data['profile_similarity']:.1%}
  • Match de skills: {match_data['skills_match']:.1%}
  • Match de experiencia: {match_data['experience_match']:.1%}
  
SCORE GENERAL: {match_data['overall_score']:.1%}

{match_data['recommendation']}

DETALLES:
{match_data['details']}
        """.strip()
        
        return response
    
    def _handle_recommendation_request(self, user_input: str) -> str:
        """Manejar request de recomendaciones"""
        
        candidate_id = None
        for c in self.candidates_db:
            if c["name"].lower() in user_input.lower():
                candidate_id = c["id"]
                break
        
        if not candidate_id:
            return "❌ No especificaste un candidato"
        
        recommendations = self.get_job_recommendations_for_candidate(candidate_id, top_k=3)
        
        response = f"""
💡 RECOMENDACIONES DE POSICIONES
═══════════════════════════════════════════

Para: {self.candidates_db[[c['id'] for c in self.candidates_db].index(candidate_id)]['name']}

"""
        for i, rec in enumerate(recommendations, 1):
            response += f"{i}. {rec['job']['title']}\n"
            response += f"   Match: {rec['overall_score']:.1%}\n"
            response += f"   {rec['recommendation']}\n\n"
        
        return response
    
    def _handle_candidates_for_job(self, user_input: str) -> str:
        """Manejar request de candidatos para una posición"""
        
        job_id = None
        for j in self.jobs_db:
            if j["title"].lower() in user_input.lower():
                job_id = j["id"]
                break
        
        if not job_id:
            return "❌ No especificaste una posición claramente"
        
        results = self.get_top_candidates_for_job(job_id, top_k=5)
        
        response = f"""
👥 TOP CANDIDATOS
═══════════════════════════════════════════

Para posición: {self.jobs_db[[j['id'] for j in self.jobs_db].index(job_id)]['title']}

"""
        for i, match in enumerate(results, 1):
            response += f"{i}. {match['candidate']['name']} - {match['overall_score']:.1%}\n"
            response += f"   {match['recommendation']}\n"
        
        return response
    
    def _show_help(self) -> str:
        """Mostrar ayuda"""
        return """
🤖 AGENTE AVANZADO DE RECRUITMENT
═══════════════════════════════════════════════════════════════════════

EJEMPLOS DE QUERIES:

1. Búsqueda:
   "Busca desarrolladores Python senior"
   "Search for machine learning engineers"

2. Matching:
   "Match Alice Johnson con Senior Backend Python Developer"
   "Cómo matchea Bob Smith con Frontend React Developer?"

3. Recomendaciones:
   "Qué posiciones recomiendas para Alice Johnson?"
   "Recommend jobs for David Lee"

4. Top Candidatos:
   "Dame los mejores candidatos para Frontend React Developer"
   "Top candidates for Machine Learning Engineer position"

═══════════════════════════════════════════════════════════════════════
        """


# =========================================================================
# MAIN: EJEMPLO DE USO
# =========================================================================

if __name__ == "__main__":
    
    # Inicializar agente (sin parámetro usa la ruta correcta automáticamente)
    agent = AdvancedRecruitmentAgent()
    
    # Test 1: Búsqueda
    print("\\n" + "="*70)
    print("TEST 1: BÚSQUEDA")
    print("="*70)
    response = agent.process_user_input("Busca desarrolladores Python senior")
    print(response)
    
    # Test 2: Matching
    print("\\n" + "="*70)
    print("TEST 2: MATCHING")
    print("="*70)
    response = agent.process_user_input("Match Alice Johnson con Senior Backend Python Developer")
    print(response)
    
    # Test 3: Recomendaciones
    print("\\n" + "="*70)
    print("TEST 3: RECOMENDACIONES")
    print("="*70)
    response = agent.process_user_input("Qué posiciones recomiendas para Alice Johnson?")
    print(response)
    
    # Test 4: Top candidatos para job
    print("\\n" + "="*70)
    print("TEST 4: TOP CANDIDATOS PARA POSICIÓN")
    print("="*70)
    response = agent.process_user_input("Dame los mejores candidatos para Senior Backend Python Developer")
    print(response)


"""
CÓMO INTEGRAR CON LANGCHAIN EN PRODUCCIÓN
════════════════════════════════════════════════

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Crear herramientas
tools = [
    Tool(
        name="Search Candidates",
        func=agent.search_candidates,
        description="Search for candidates based on a query"
    ),
    Tool(
        name="Match Candidate to Job",
        func=lambda args: agent.calculate_candidate_job_match(args.split(",")[0], args.split(",")[1]),
        description="Calculate match between candidate and job"
    ),
    Tool(
        name="Get Recommendations",
        func=agent.get_job_recommendations_for_candidate,
        description="Get job recommendations for a candidate"
    ),
]

# Crear agente con LLM
llm = OpenAI(temperature=0.7)
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Usar
response = agent.run("Find the best candidates for a Senior Python Developer position")

════════════════════════════════════════════════════════════════════════
"""
