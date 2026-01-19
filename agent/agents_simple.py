"""
AGENTE SIMPLE CON REGLAS (SIN LLM)
Nivel: Beginner
Complejidad: Baja
Dependencias: loader.py (tu modelo)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loader import load_model
from typing import List, Dict
import re


class SimpleRecruitmentAgent:
    """Agente básico usando reglas y el modelo"""
    
    def __init__(self, model_path: str = None):
        """Inicializar agente"""
        if model_path is None:
            # Usar ruta relativa al proyecto raíz
            project_root = Path(__file__).parent.parent
            model_path = str(project_root / "model")
        self.model = load_model(model_path)
        
        # Base de datos de ejemplo (en producción sería una DB real)
        self.candidates_db = [
            "Senior Python Developer with 10 years experience",
            "Python backend engineer specializing in APIs",
            "Junior Python developer learning Django",
            "Java Software Engineer with Spring Boot",
            "Frontend Developer expert in React and Vue",
            "Data Scientist specialized in Machine Learning",
            "DevOps Engineer with Kubernetes experience",
            "Full Stack Developer Python and React",
            "Cloud Architect AWS certified",
            "QA Automation Engineer Selenium",
        ]
        
        self.jobs_db = [
            "Senior Backend Python Developer - 5-10 years experience required",
            "Frontend React Developer - UI/UX focused",
            "ML Engineer - Python and TensorFlow required",
            "DevOps Engineer - Kubernetes and Docker",
            "Full Stack Developer - Python and React",
        ]
        
        print("✅ Agente de Recruitment inicializado")
        print(f"   Candidatos en DB: {len(self.candidates_db)}")
        print(f"   Posiciones en DB: {len(self.jobs_db)}\n")
    
    # =========================================================================
    # MÉTODO PRINCIPAL
    # =========================================================================
    
    def process_query(self, user_query: str) -> str:
        """
        Procesa una query del usuario y retorna respuesta
        
        Soporta:
        - "busca": buscar candidatos
        - "match" o "matches": matching job-candidate
        - "similar": similitud entre dos textos
        - "agrupa": agrupar candidatos
        - "info": información sobre el agente
        """
        query_lower = user_query.lower().strip()
        
        # Detectar intent basado en palabras clave
        if any(word in query_lower for word in ["busca", "encuentra", "search"]):
            return self._handle_search(user_query)
        
        elif any(word in query_lower for word in ["match", "matchea", "matching"]):
            return self._handle_matching(user_query)
        
        elif any(word in query_lower for word in ["similar", "parecido", "similarity"]):
            return self._handle_similarity(user_query)
        
        elif any(word in query_lower for word in ["agrupa", "grupo", "cluster"]):
            return self._handle_clustering(user_query)
        
        elif any(word in query_lower for word in ["info", "ayuda", "help"]):
            return self._show_help()
        
        else:
            return self._show_help()
    
    # =========================================================================
    # HANDLERS: BÚSQUEDA
    # =========================================================================
    
    def _handle_search(self, query: str) -> str:
        """Manejar búsqueda de candidatos"""
        
        # Extraer palabras clave
        search_terms = self._extract_search_terms(query)
        
        if not search_terms:
            return "❌ No encontré qué buscar. Ejemplo: 'Busca desarrollador Python senior'"
        
        # Buscar candidatos
        results = self.model.search(
            search_terms,
            self.candidates_db,
            top_k=5
        )
        
        # Formatear resultados
        response = f"🔎 Resultados para: '{search_terms}'\n\n"
        for i, result in enumerate(results, 1):
            score_percent = result['similarity'] * 100
            score_bar = "█" * int(score_percent / 10) + "░" * (10 - int(score_percent / 10))
            response += f"{i}. {result['candidate']}\n"
            response += f"   [{score_bar}] {score_percent:.1f}%\n\n"
        
        return response
    
    def _extract_search_terms(self, query: str) -> str:
        """Extrae términos de búsqueda de una query"""
        
        # Patrones comunes
        patterns = [
            r"busca\s+(?:un?\s+)?(.+?)(?:\?|$|\.)",
            r"encuentra\s+(?:un?\s+)?(.+?)(?:\?|$|\.)",
            r"search\s+(?:for\s+)?(.+?)(?:\?|$|\.)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                return match.group(1).strip()
        
        # Si no hay patrón, usa toda la query sin palabras clave
        query_clean = re.sub(r"(busca|encuentra|search|para|para\s+un|para\s+una)", "", query)
        return query_clean.strip()
    
    # =========================================================================
    # HANDLERS: MATCHING
    # =========================================================================
    
    def _handle_matching(self, query: str) -> str:
        """Manejar matching entre posición y candidato"""
        
        # Intentar extraer job y candidate de la query
        # Formato esperado: "Match: 'Senior Developer' con 'John Developer'"
        
        parts = re.findall(r"['\"](.+?)['\"]", query)
        
        if len(parts) >= 2:
            job = parts[0]
            candidate = parts[1]
        else:
            return "❌ Formato incorrecto. Ejemplo: \"Match: 'Senior Developer' con 'Python Engineer'\""
        
        # Calcular similitud
        score = self.model.similarity(job, candidate)
        
        # Interpretar resultado
        if score > 0.8:
            interpretation = "🟢 Excelente match"
        elif score > 0.6:
            interpretation = "🟡 Buen match"
        elif score > 0.4:
            interpretation = "🟠 Match moderado"
        else:
            interpretation = "🔴 Bajo match"
        
        response = f"📊 Matching: '{job}' vs '{candidate}'\n\n"
        response += f"Score: {score:.2%} {interpretation}\n"
        response += f"\nInterpretación:\n"
        
        if score > 0.8:
            response += "✅ Candidato es altamente relevante para esta posición"
        elif score > 0.6:
            response += "✅ Candidato tiene buena relevancia"
        elif score > 0.4:
            response += "⚠️ Candidato tiene cierta relevancia pero no es ideal"
        else:
            response += "❌ Candidato no es relevante para esta posición"
        
        return response
    
    # =========================================================================
    # HANDLERS: SIMILITUD
    # =========================================================================
    
    def _handle_similarity(self, query: str) -> str:
        """Manejar cálculo de similitud entre textos"""
        
        # Extraer dos textos de la query
        parts = re.findall(r"['\"](.+?)['\"]", query)
        
        if len(parts) >= 2:
            text1 = parts[0]
            text2 = parts[1]
        else:
            return "❌ Formato incorrecto. Ejemplo: \"Similar: 'texto1' y 'texto2'\""
        
        # Calcular similitud
        score = self.model.similarity(text1, text2)
        
        response = f"📐 Similitud entre:\n"
        response += f"  1. '{text1}'\n"
        response += f"  2. '{text2}'\n\n"
        response += f"Score: {score:.4f} ({score*100:.2f}%)\n"
        
        if score > 0.8:
            response += "\n🟢 Muy similares - casi idénticos"
        elif score > 0.6:
            response += "\n🟡 Bastante similares"
        elif score > 0.4:
            response += "\n🟠 Moderadamente similares"
        else:
            response += "\n🔴 Muy diferentes"
        
        return response
    
    # =========================================================================
    # HANDLERS: CLUSTERING
    # =========================================================================
    
    def _handle_clustering(self, query: str) -> str:
        """Manejar agrupación de candidatos"""
        
        # Extraer número de clusters de la query
        match = re.search(r"(\d+)\s*grupo", query.lower())
        n_clusters = int(match.group(1)) if match else 3
        
        # Asegurar que n_clusters sea válido
        n_clusters = min(max(2, n_clusters), len(self.candidates_db))
        
        # Realizar clustering
        clusters = self.model.cluster(self.candidates_db, n_clusters=n_clusters)
        
        response = f"🎯 Clustering: {len(self.candidates_db)} candidatos en {len(clusters)} grupos\n\n"
        
        for cluster_id, candidates in clusters.items():
            response += f"📌 Grupo {cluster_id + 1}:\n"
            for candidate in candidates:
                response += f"   • {candidate}\n"
            response += "\n"
        
        return response
    
    # =========================================================================
    # AYUDA
    # =========================================================================
    
    def _show_help(self) -> str:
        """Mostrar ayuda sobre comandos disponibles"""
        
        help_text = """
🤖 AGENTE DE RECRUITMENT - COMANDOS DISPONIBLES
═════════════════════════════════════════════════

1️⃣  BÚSQUEDA DE CANDIDATOS
   Ejemplo: "Busca un desarrollador Python senior"
   Resultado: Lista rankeada de candidatos más similares
   
2️⃣  MATCHING JOB-CANDIDATE
   Ejemplo: "Match: 'Senior Developer' con 'Python Engineer'"
   Resultado: Score de similitud y análisis
   
3️⃣  SIMILITUD ENTRE TEXTOS
   Ejemplo: "Similar: 'java developer' y 'java programmer'"
   Resultado: Score de similitud (0-1)
   
4️⃣  CLUSTERING/AGRUPACIÓN
   Ejemplo: "Agrupa candidatos en 3 grupos"
   Resultado: Candidatos agrupados por similitud
   
5️⃣  INFORMACIÓN
   Ejemplo: "Info" o "Ayuda"
   Resultado: Este mensaje
   
═════════════════════════════════════════════════════════════════════════════

💡 TIPS:
  • Sé específico en tus búsquedas
  • Usa palabras clave del dominio de recruitment
  • Para matching, envuelve en comillas: "texto1" y "texto2"
        """
        return help_text


# =========================================================================
# MAIN: EJEMPLO DE USO
# =========================================================================

if __name__ == "__main__":
    
    # Inicializar agente (sin parámetro usa la ruta correcta automáticamente)
    agent = SimpleRecruitmentAgent()
    
    # Test 1: Búsqueda
    print("=" * 70)
    print("TEST 1: BÚSQUEDA DE CANDIDATOS")
    print("=" * 70)
    query1 = "Busca un desarrollador Python senior"
    print(f"User: {query1}\n")
    response1 = agent.process_query(query1)
    print(response1)
    
    # Test 2: Matching
    print("\n" + "=" * 70)
    print("TEST 2: MATCHING JOB-CANDIDATE")
    print("=" * 70)
    query2 = "Match: 'Senior Backend Python Developer' con 'Python backend engineer'"
    print(f"User: {query2}\n")
    response2 = agent.process_query(query2)
    print(response2)
    
    # Test 3: Similitud
    print("\n" + "=" * 70)
    print("TEST 3: SIMILITUD")
    print("=" * 70)
    query3 = "Similar: 'developer' y 'engineer'"
    print(f"User: {query3}\n")
    response3 = agent.process_query(query3)
    print(response3)
    
    # Test 4: Clustering
    print("\n" + "=" * 70)
    print("TEST 4: CLUSTERING")
    print("=" * 70)
    query4 = "Agrupa candidatos en 3 grupos"
    print(f"User: {query4}\n")
    response4 = agent.process_query(query4)
    print(response4)
    
    # Test 5: Ayuda
    print("\n" + "=" * 70)
    print("TEST 5: AYUDA")
    print("=" * 70)
    query5 = "Info"
    print(f"User: {query5}\n")
    response5 = agent.process_query(query5)
    print(response5)


"""
CÓMO USAR EN TU APLICACIÓN
═════════════════════════════

1. Desde Python:
   ───────────────
   from simple_agent import SimpleRecruitmentAgent
   
   agent = SimpleRecruitmentAgent("./model")
   response = agent.process_query("Busca un Python developer")
   print(response)

2. Como API REST (con FastAPI):
   ──────────────────────────────
   from fastapi import FastAPI
   from simple_agent import SimpleRecruitmentAgent
   
   app = FastAPI()
   agent = SimpleRecruitmentAgent("./model")
   
   @app.post("/query")
   async def query(text: str):
       response = agent.process_query(text)
       return {"response": response}
   
   # Ejecutar: uvicorn app:app --reload

3. Conversacional (loop):
   ───────────────────────
   agent = SimpleRecruitmentAgent("./model")
   
   while True:
       user_input = input("You: ")
       if user_input.lower() == "salir":
           break
       response = agent.process_query(user_input)
       print(f"Agent: {response}")

═════════════════════════════════════════════════════════════════════════
"""
