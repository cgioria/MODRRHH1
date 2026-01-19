#!/usr/bin/env python3
"""
Ejemplo 2: Cliente API
=====================

Demuestra cómo usar el modelo a través de la API REST.

Primero, inicia el servidor con:
    python api_wrapper.py --port 8000

Luego ejecuta este script en otra terminal.
"""

import requests
import json
import time


BASE_URL = "http://localhost:8000"


def print_section(title):
    """Imprimir sección formateada"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def ejemplo_1_health_check():
    """Verificar que el servidor está activo"""
    print_section("1. Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Servidor activo")
            print(f"   Status: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
            return False
        return True
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print(f"   Asegúrate de que está ejecutándose:")
        print(f"   python api_wrapper.py --port 8000")
        return False


def ejemplo_2_info():
    """Obtener información del modelo"""
    print_section("2. Información del Modelo")
    
    try:
        response = requests.get(f"{BASE_URL}/info")
        info = response.json()
        
        print("\n📋 Metadatos:")
        print(json.dumps(info, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_3_embed():
    """Generar embeddings"""
    print_section("3. Generar Embeddings")
    
    try:
        textos = [
            "python developer",
            "java engineer",
            "fullstack"
        ]
        
        print(f"\n📝 Generando embeddings para {len(textos)} textos:")
        for t in textos:
            print(f"   • {t}")
        
        response = requests.post(f"{BASE_URL}/embed", json={"texts": textos})
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Embeddings generados:")
            print(f"   Cantidad: {len(data['embeddings'])}")
            print(f"   Dimensión: {len(data['embeddings'][0])}")
            print(f"\n   Primeros 5 valores del primer embedding:")
            print(f"   {data['embeddings'][0][:5]}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_4_similarity():
    """Calcular similitud"""
    print_section("4. Similitud entre Textos")
    
    try:
        pares = [
            ("python developer", "python engineer"),
            ("python developer", "java developer"),
            ("senior developer", "junior developer"),
        ]
        
        print(f"\n🔄 Calculando similitud para {len(pares)} pares:\n")
        
        for text1, text2 in pares:
            response = requests.post(f"{BASE_URL}/similarity", json={
                "text1": text1,
                "text2": text2
            })
            
            if response.status_code == 200:
                data = response.json()
                sim = data['similarity']
                print(f"   '{text1}' vs '{text2}'")
                print(f"   → Similitud: {sim:.4f} ({sim*100:.2f}%)")
                print()
            else:
                print(f"❌ Error: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_5_search():
    """Búsqueda de candidatos"""
    print_section("5. Búsqueda de Candidatos")
    
    try:
        query = "python senior developer"
        candidates = [
            "java programmer",
            "python engineer",
            "fullstack javascript",
            "python specialist",
            "frontend react",
            "devops engineer",
            "data scientist",
            "cloud architect"
        ]
        
        print(f"\n🔍 Búsqueda: '{query}'")
        print(f"   Entre {len(candidates)} candidatos")
        
        response = requests.post(f"{BASE_URL}/search", json={
            "query": query,
            "candidates": candidates,
            "top_k": 3
        })
        
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            
            print(f"\n   Top {len(results)} resultados:\n")
            for i, result in enumerate(results, 1):
                sim = result['similarity']
                cand = result['candidate']
                print(f"   {i}. {cand}")
                print(f"      Similitud: {sim:.4f} ({sim*100:.2f}%)")
                print(f"      {'⭐' * int(sim * 5)}\n")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_6_cluster():
    """Clustering"""
    print_section("6. Clustering de Textos")
    
    try:
        textos = [
            "python developer",
            "python engineer",
            "java developer",
            "java programmer",
            "frontend react",
            "frontend angular",
            "devops engineer",
            "cloud architect"
        ]
        
        print(f"\n📦 Agrupando {len(textos)} textos en 3 clusters:")
        for i, t in enumerate(textos, 1):
            print(f"   {i}. {t}")
        
        response = requests.post(f"{BASE_URL}/cluster", json={
            "texts": textos,
            "n_clusters": 3
        })
        
        if response.status_code == 200:
            data = response.json()
            clusters = data['clusters']
            
            print(f"\n✅ Clustering completado:\n")
            for cluster_id, miembros in enumerate(clusters, 1):
                print(f"   Cluster {cluster_id}:")
                for miembro in miembros:
                    print(f"      • {miembro}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_7_performance():
    """Medir rendimiento"""
    print_section("7. Rendimiento de la API")
    
    try:
        print("\n⏱️ Midiendo tiempos de respuesta...\n")
        
        # Test embedding
        start = time.time()
        requests.post(f"{BASE_URL}/embed", json={
            "texts": ["test"] * 10
        })
        embed_time = (time.time() - start) * 1000
        
        # Test similarity
        start = time.time()
        requests.post(f"{BASE_URL}/similarity", json={
            "text1": "test",
            "text2": "test"
        })
        sim_time = (time.time() - start) * 1000
        
        # Test search
        start = time.time()
        requests.post(f"{BASE_URL}/search", json={
            "query": "test",
            "candidates": ["test"] * 10
        })
        search_time = (time.time() - start) * 1000
        
        print(f"   Embedding (10 textos): {embed_time:.2f}ms")
        print(f"   Similitud: {sim_time:.2f}ms")
        print(f"   Búsqueda (10 candidatos): {search_time:.2f}ms")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_8_swagger():
    """Documentación interactiva"""
    print_section("8. Documentación Interactiva")
    
    print("\n📚 Accede a la documentación interactiva de Swagger en:")
    print(f"   {BASE_URL}/docs")
    print("\n   Allí puedes:")
    print("   • Ver todos los endpoints disponibles")
    print("   • Probar la API interactivamente")
    print("   • Ver el esquema de peticiones y respuestas")
    print("   • Ver ejemplos de uso")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "🚀 CLIENTE API - EJEMPLOS DE USO\n".center(60, "="))
    
    # Verificar que el servidor está activo
    if not ejemplo_1_health_check():
        print("\n⚠️ El servidor no está disponible")
        print("\nInicia el servidor con:")
        print("   python api_wrapper.py --port 8000\n")
        return
    
    try:
        ejemplo_2_info()
        ejemplo_3_embed()
        ejemplo_4_similarity()
        ejemplo_5_search()
        ejemplo_6_cluster()
        ejemplo_7_performance()
        ejemplo_8_swagger()
        
        print("\n" + "✅ TODOS LOS EJEMPLOS COMPLETADOS".center(60, "=") + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
