#!/usr/bin/env python3
"""
Ejemplo 1: Uso directo en Python
================================

Demuestra cómo usar el modelo entrenado directamente en tu código Python.
"""

import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loader import load_model
import json


def ejemplo_1_embedding():
    """Ejemplo 1: Generar embeddings para textos"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Generar Embeddings")
    print("="*60)
    
    model = load_model("./model")
    
    textos = [
        "desarrollador python senior",
        "ingeniero de software java",
        "fullstack javascript react"
    ]
    
    print("\nGenerando embeddings para:")
    for texto in textos:
        embedding = model.encode(texto)
        print(f"\n📝 '{texto}'")
        print(f"   Dimensiones: {embedding.shape}")
        print(f"   Primeros 5 valores: {embedding[:5]}")
        print(f"   Media: {embedding.mean():.6f}")
        print(f"   Desv. Est.: {embedding.std():.6f}")


def ejemplo_2_similitud():
    """Ejemplo 2: Calcular similitud entre textos"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Similitud entre Textos")
    print("="*60)
    
    model = load_model("./model")
    
    pares = [
        ("python developer", "python engineer"),
        ("python developer", "java developer"),
        ("senior developer", "junior engineer"),
        ("senior developer", "senior architect"),
    ]
    
    print("\nCalculando similitud entre pares:")
    for texto1, texto2 in pares:
        score = model.similarity(texto1, texto2)
        print(f"\n📊 '{texto1}' vs '{texto2}'")
        print(f"   Similitud: {score:.4f} ({score*100:.2f}%)")
        
        # Interpretar el resultado
        if score > 0.8:
            interpretation = "Muy similar ✅"
        elif score > 0.6:
            interpretation = "Similar ⚠️"
        elif score > 0.4:
            interpretation = "Poco similar"
        else:
            interpretation = "Muy diferente ❌"
        print(f"   Interpretación: {interpretation}")


def ejemplo_3_busqueda():
    """Ejemplo 3: Buscar candidatos similares"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Búsqueda de Candidatos")
    print("="*60)
    
    model = load_model("./model")
    
    # Simulamos una búsqueda de candidatos
    query = "python senior developer"
    
    candidatos = [
        "java developer",
        "python engineer",
        "fullstack javascript",
        "python specialist",
        "python architect",
        "javascript developer",
        "react developer",
        "backend engineer"
    ]
    
    print(f"\n🔍 Búsqueda: '{query}'")
    print(f"   Entre {len(candidatos)} candidatos")
    
    # Búsqueda simple
    resultados = model.search(query, candidatos, top_k=3)
    
    print(f"\n   Top 3 resultados:")
    for i, resultado in enumerate(resultados, 1):
        score = resultado['similarity']
        candidato = resultado['candidate']
        print(f"\n   {i}. {candidato}")
        print(f"      Similitud: {score:.4f} ({score*100:.2f}%)")
        print(f"      Ranking: {'⭐' * int(score * 5)}")


def ejemplo_4_clustering():
    """Ejemplo 4: Agrupar textos en clusters"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Clustering de Textos")
    print("="*60)
    
    model = load_model("./model")
    
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
    
    print(f"\nAgrupando {len(textos)} textos en 3 clusters...")
    
    clusters = model.cluster(textos, n_clusters=3)
    
    print(f"\n📦 Resultados del clustering:")
    for cluster_id, miembros in clusters.items():
        print(f"\nCluster {cluster_id + 1}:")
        for miembro in miembros:
            print(f"   • {miembro}")


def ejemplo_5_batch_processing():
    """Ejemplo 5: Procesamiento en batch"""
    print("\n" + "="*60)
    print("EJEMPLO 5: Procesamiento en Batch")
    print("="*60)
    
    model = load_model("./model")
    
    # Generar múltiples embeddings de una vez es más eficiente
    textos = [
        "text1", "text2", "text3", "text4", "text5",
        "text6", "text7", "text8", "text9", "text10"
    ]
    
    print(f"\nGenerando {len(textos)} embeddings...")
    
    embeddings = model.encode(textos)
    
    print(f"✅ Generados {len(embeddings)} embeddings")
    print(f"   Shape: {embeddings.shape}")
    
    # Calcular similitud entre embeddings
    print(f"\nCalculando matriz de similitud...")
    import numpy as np
    
    matriz_similitud = np.zeros((len(embeddings), len(embeddings)))
    for i in range(len(embeddings)):
        for j in range(len(embeddings)):
            matriz_similitud[i][j] = np.dot(embeddings[i], embeddings[j])
    
    print(f"✅ Matriz de similitud calculada {matriz_similitud.shape}")
    print(f"   Valor mínimo: {matriz_similitud.min():.4f}")
    print(f"   Valor máximo: {matriz_similitud.max():.4f}")
    print(f"   Valor medio: {matriz_similitud.mean():.4f}")


def ejemplo_6_metadata():
    """Ejemplo 6: Obtener información del modelo"""
    print("\n" + "="*60)
    print("EJEMPLO 6: Información del Modelo")
    print("="*60)
    
    model = load_model("./model")
    
    info = model.get_info()
    
    print("\n📋 Información del modelo:")
    print(json.dumps(info, indent=2, ensure_ascii=False))


def ejemplo_7_produccion():
    """Ejemplo 7: Patrón para producción"""
    print("\n" + "="*60)
    print("EJEMPLO 7: Patrón Producción")
    print("="*60)
    
    # En producción, cargas el modelo UNA SOLA VEZ
    print("\n⚙️ Inicializando modelo (una sola vez)...")
    model = load_model("./model")
    
    print("✅ Modelo cargado en memoria\n")
    
    # Luego reutilizas para múltiples operaciones
    operaciones = [
        ("embed", "python developer"),
        ("similarity", "python", "java"),
        ("search", "senior", ["python", "java", "fullstack"]),
    ]
    
    print("Realizando operaciones:")
    
    # 1. Embedding
    print("\n1️⃣ Generar embedding...")
    embedding = model.encode("python developer")
    print(f"   ✅ Embedding generado: {embedding.shape}")
    
    # 2. Similitud
    print("\n2️⃣ Calcular similitud...")
    sim = model.similarity("python", "java")
    print(f"   ✅ Similitud: {sim:.4f}")
    
    # 3. Búsqueda
    print("\n3️⃣ Buscar candidatos...")
    results = model.search("senior", ["python", "java", "fullstack"], top_k=2)
    print(f"   ✅ Encontrados {len(results)} resultados")
    
    print("\n✨ Todas las operaciones completadas exitosamente")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "🚀 EJEMPLOS DE USO DEL MODELO ENTRENADO\n".center(60, "="))
    
    try:
        ejemplo_1_embedding()
        ejemplo_2_similitud()
        ejemplo_3_busqueda()
        ejemplo_4_clustering()
        ejemplo_5_batch_processing()
        ejemplo_6_metadata()
        ejemplo_7_produccion()
        
        print("\n" + "✅ TODOS LOS EJEMPLOS COMPLETADOS".center(60, "=") + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
