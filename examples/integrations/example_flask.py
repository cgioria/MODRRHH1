#!/usr/bin/env python3
"""
Ejemplo 4: Integración en Flask
==============================

Demuestra cómo integrar el modelo en una aplicación Flask.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import sys

# Importar el modelo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loader import load_model


# Crear aplicación Flask
app = Flask(__name__)
CORS(app)

# Cargar modelo una sola vez
print("Cargando modelo...")
model = load_model("./model")
print("✅ Modelo cargado")


# ============================================================================
# MODELOS DE DATOS
# ============================================================================

class Candidate:
    """Clase para representar un candidato"""
    def __init__(self, id, name, title, skills, experience):
        self.id = id
        self.name = name
        self.title = title
        self.skills = skills
        self.experience = experience
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'skills': self.skills,
            'experience': self.experience
        }
    
    def get_profile_text(self):
        """Generar texto del perfil para el modelo"""
        return f"{self.title} {self.skills} {self.experience}"


# Base de datos simulada
CANDIDATES = [
    Candidate(1, "Juan García", "Python Developer", "python, django, postgresql", "5 años"),
    Candidate(2, "María López", "Python Engineer", "python, fastapi, aws", "7 años"),
    Candidate(3, "Carlos Ruiz", "Java Developer", "java, spring, sql", "4 años"),
    Candidate(4, "Ana Martínez", "Fullstack", "javascript, react, node, mongodb", "6 años"),
    Candidate(5, "Luis Fernández", "DevOps Engineer", "docker, kubernetes, aws, cicd", "5 años"),
    Candidate(6, "Elena Sánchez", "Frontend Developer", "react, typescript, css", "3 años"),
    Candidate(7, "Roberto Díaz", "Senior Python", "python, machine learning, pytorch", "8 años"),
]


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return jsonify({
        'status': 'ok',
        'message': 'API de Búsqueda de Candidatos',
        'endpoints': {
            'GET /': 'Esta página',
            'GET /health': 'Health check',
            'POST /api/search': 'Buscar candidatos similares',
            'POST /api/similarity': 'Calcular similitud entre dos candidatos',
            'GET /api/cluster': 'Agrupar candidatos',
            'GET /api/candidates': 'Listar todos los candidatos',
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'message': 'API healthy'})


@app.route('/api/candidates', methods=['GET'])
def list_candidates():
    """Listar todos los candidatos"""
    return jsonify({
        'total': len(CANDIDATES),
        'candidates': [c.to_dict() for c in CANDIDATES]
    })


@app.route('/api/search', methods=['POST'])
def search_candidates():
    """
    Buscar candidatos similares
    
    JSON requerido:
    {
        "query": "descripción del puesto",
        "top_k": 5
    }
    """
    try:
        data = request.get_json()
        query = data.get('query')
        top_k = data.get('top_k', 5)
        
        if not query:
            return jsonify({'error': 'Query requerida'}), 400
        
        # Generar textos de perfiles
        candidate_texts = [c.get_profile_text() for c in CANDIDATES]
        
        # Buscar
        results = model.search(query, candidate_texts, top_k=min(top_k, len(CANDIDATES)))
        
        # Formatear respuesta
        formatted_results = []
        for result in results:
            # Encontrar candidato
            for i, candidate_text in enumerate(candidate_texts):
                if candidate_text == result['candidate']:
                    candidate = CANDIDATES[i]
                    formatted_results.append({
                        'candidate': candidate.to_dict(),
                        'similarity': round(result['similarity'], 4),
                        'match_percentage': round(result['similarity'] * 100, 2)
                    })
                    break
        
        return jsonify({
            'query': query,
            'total_candidates': len(CANDIDATES),
            'results_found': len(formatted_results),
            'results': formatted_results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/similarity', methods=['POST'])
def calculate_similarity():
    """
    Calcular similitud entre dos candidatos
    
    JSON requerido:
    {
        "candidate_id_1": 1,
        "candidate_id_2": 2
    }
    """
    try:
        data = request.get_json()
        id1 = data.get('candidate_id_1')
        id2 = data.get('candidate_id_2')
        
        if not id1 or not id2:
            return jsonify({'error': 'IDs de candidatos requeridos'}), 400
        
        # Encontrar candidatos
        cand1 = next((c for c in CANDIDATES if c.id == id1), None)
        cand2 = next((c for c in CANDIDATES if c.id == id2), None)
        
        if not cand1 or not cand2:
            return jsonify({'error': 'Candidato no encontrado'}), 404
        
        # Calcular similitud
        similarity = model.similarity(
            cand1.get_profile_text(),
            cand2.get_profile_text()
        )
        
        return jsonify({
            'candidate_1': cand1.to_dict(),
            'candidate_2': cand2.to_dict(),
            'similarity': round(similarity, 4),
            'match_percentage': round(similarity * 100, 2)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cluster', methods=['GET'])
def cluster_candidates():
    """
    Agrupar candidatos por similitud
    
    Parámetros GET:
    - n_clusters: número de clusters (default: 3)
    """
    try:
        n_clusters = int(request.args.get('n_clusters', 3))
        
        if n_clusters > len(CANDIDATES):
            n_clusters = len(CANDIDATES)
        
        if n_clusters < 1:
            return jsonify({'error': 'n_clusters debe ser >= 1'}), 400
        
        # Generar textos
        candidate_texts = [c.get_profile_text() for c in CANDIDATES]
        
        # Clustering
        clusters = model.cluster(candidate_texts, n_clusters=n_clusters)
        
        # Formatear respuesta
        formatted_clusters = []
        for cluster_id, members in enumerate(clusters):
            cluster_data = {
                'id': cluster_id + 1,
                'members': []
            }
            
            for member_text in members:
                for i, candidate_text in enumerate(candidate_texts):
                    if candidate_text == member_text:
                        cluster_data['members'].append(CANDIDATES[i].to_dict())
                        break
            
            formatted_clusters.append(cluster_data)
        
        return jsonify({
            'n_clusters': n_clusters,
            'clusters': formatted_clusters
        })
    
    except ValueError:
        return jsonify({'error': 'n_clusters debe ser un número'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/profile/<int:candidate_id>', methods=['GET'])
def get_profile(candidate_id):
    """Obtener perfil de un candidato"""
    try:
        candidate = next((c for c in CANDIDATES if c.id == candidate_id), None)
        
        if not candidate:
            return jsonify({'error': 'Candidato no encontrado'}), 404
        
        return jsonify(candidate.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500


# ============================================================================
# INICIALIZAR APLICACIÓN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  API DE BÚSQUEDA DE CANDIDATOS")
    print("="*60)
    print(f"\n📍 Iniciando servidor en http://localhost:5000")
    print(f"\n📚 Documentación: http://localhost:5000")
    print(f"📝 Total candidatos: {len(CANDIDATES)}\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
