#!/usr/bin/env python3
"""
Ejemplo 3: Integración en Django
================================

Demuestra cómo integrar el modelo en una aplicación Django.
"""

# settings.py
"""
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'candidates',
]

# Cargar modelo al iniciar Django
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = os.path.join(BASE_DIR, 'modelo_entrenado_multiloss_portable')

from loader import load_model
MODELO = load_model(MODEL_PATH)
"""


# models.py
from django.db import models


class Candidate(models.Model):
    """Modelo de candidato"""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    skills = models.TextField()  # JSON o texto separado por comas
    cv_text = models.TextField()  # Texto extraído del CV
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.title}"


class JobPosting(models.Model):
    """Modelo de puesto de trabajo"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.views import View
import json


class SearchCandidatesView(View):
    """
    Vista para buscar candidatos similares a una descripción de puesto
    """
    
    def post(self, request):
        """
        POST /api/search/
        
        Parámetros JSON:
        - query: descripción del puesto
        - limit: cantidad máxima de resultados (default: 10)
        """
        try:
            data = json.loads(request.body)
            query = data.get('query')
            limit = data.get('limit', 10)
            
            if not query:
                return JsonResponse({'error': 'Query requerida'}, status=400)
            
            # Obtener todos los candidatos
            candidates = Candidate.objects.all()
            candidate_texts = [
                f"{c.title} - {c.skills}" for c in candidates
            ]
            
            # Buscar candidatos similares usando el modelo
            results = settings.MODELO.search(query, candidate_texts, top_k=limit)
            
            # Formatear respuesta
            response_data = {
                'query': query,
                'total': len(candidates),
                'found': len(results),
                'results': []
            }
            
            for result in results:
                # Encontrar el candidato correspondiente
                for i, c in enumerate(candidates):
                    if candidate_texts[i] == result['candidate']:
                        response_data['results'].append({
                            'id': c.id,
                            'name': c.name,
                            'title': c.title,
                            'similarity': round(result['similarity'], 4),
                            'match_percentage': round(result['similarity'] * 100, 2)
                        })
                        break
            
            return JsonResponse(response_data)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CandidateSimilarityView(View):
    """
    Vista para calcular similitud entre dos candidatos
    """
    
    def post(self, request):
        """
        POST /api/similarity/
        
        Parámetros JSON:
        - candidate_id_1: ID del primer candidato
        - candidate_id_2: ID del segundo candidato
        """
        try:
            data = json.loads(request.body)
            cand_id_1 = data.get('candidate_id_1')
            cand_id_2 = data.get('candidate_id_2')
            
            if not cand_id_1 or not cand_id_2:
                return JsonResponse({'error': 'IDs de candidatos requeridos'}, status=400)
            
            # Obtener candidatos
            c1 = get_object_or_404(Candidate, id=cand_id_1)
            c2 = get_object_or_404(Candidate, id=cand_id_2)
            
            # Calcular similitud
            text1 = f"{c1.title} - {c1.skills}"
            text2 = f"{c2.title} - {c2.skills}"
            similarity = settings.MODELO.similarity(text1, text2)
            
            return JsonResponse({
                'candidate_1': {
                    'id': c1.id,
                    'name': c1.name,
                    'title': c1.title
                },
                'candidate_2': {
                    'id': c2.id,
                    'name': c2.name,
                    'title': c2.title
                },
                'similarity': round(similarity, 4),
                'match_percentage': round(similarity * 100, 2)
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ClusterCandidatesView(View):
    """
    Vista para agrupar candidatos por similitud
    """
    
    def get(self, request):
        """
        GET /api/cluster/
        
        Parámetros GET:
        - n_clusters: número de clusters (default: 3)
        """
        try:
            n_clusters = int(request.GET.get('n_clusters', 3))
            
            # Obtener todos los candidatos
            candidates = Candidate.objects.all()
            candidate_texts = [
                f"{c.title} - {c.skills}" for c in candidates
            ]
            
            if not candidate_texts:
                return JsonResponse({'error': 'No hay candidatos'}, status=400)
            
            # Clustering
            clusters = settings.MODELO.cluster(candidate_texts, n_clusters=n_clusters)
            
            # Formatear respuesta
            response_data = {
                'n_clusters': n_clusters,
                'clusters': []
            }
            
            for cluster_id, members in enumerate(clusters):
                cluster_data = {
                    'id': cluster_id + 1,
                    'members': []
                }
                
                for member_text in members:
                    for i, c in enumerate(candidates):
                        if candidate_texts[i] == member_text:
                            cluster_data['members'].append({
                                'id': c.id,
                                'name': c.name,
                                'title': c.title
                            })
                            break
                
                response_data['clusters'].append(cluster_data)
            
            return JsonResponse(response_data)
            
        except ValueError:
            return JsonResponse({'error': 'n_clusters debe ser un número'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# urls.py
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/search/', views.SearchCandidatesView.as_view(), name='search'),
    path('api/similarity/', views.CandidateSimilarityView.as_view(), name='similarity'),
    path('api/cluster/', views.ClusterCandidatesView.as_view(), name='cluster'),
]


# Uso desde template
"""
<!-- template -->
<form id="searchForm">
    <input type="text" id="query" placeholder="Descripción del puesto">
    <button type="submit">Buscar</button>
</form>

<div id="results"></div>

<script>
document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = document.getElementById('query').value;
    
    const response = await fetch('/api/search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ query: query, limit: 10 })
    });
    
    const data = await response.json();
    
    let html = `<h3>Resultados (${data.found}/${data.total})</h3>`;
    html += '<ul>';
    
    data.results.forEach(r => {
        html += `<li>${r.name} (${r.title}) - ${r.match_percentage}% match</li>`;
    });
    
    html += '</ul>';
    
    document.getElementById('results').innerHTML = html;
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
</script>
"""
