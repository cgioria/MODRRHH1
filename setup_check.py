#!/usr/bin/env python3
"""
Script de Verificación de Setup
Ejecutar después de clonar el repositorio para verificar que todo funciona
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"🔍 {text}")
    print(f"{'='*60}\n")

def check_file(path, description):
    exists = Path(path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_python_package(package_name, import_name=None):
    import_name = import_name or package_name
    try:
        __import__(import_name)
        print(f"✅ {package_name} instalado")
        return True
    except ImportError:
        print(f"❌ {package_name} NO instalado - ejecutar: pip install -r requirements.txt")
        return False

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     VERIFICACIÓN DE SETUP - RECRUITMENT MODEL              ║
    ║     Ejecutar después de: git clone + pip install           ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    all_ok = True
    
    # 1. Verificar archivos críticos
    print_header("1️⃣  ARCHIVOS CRÍTICOS")
    
    critical_files = [
        ("loader.py", "Core del modelo"),
        ("requirements.txt", "Dependencias"),
        ("README.md", "Documentación principal"),
        ("QUICKSTART.md", "Guía rápida"),
        ("model/model.safetensors", "Modelo entrenado (Git LFS)"),
        ("agent/agents_simple.py", "Agente simple"),
        ("agent/agents_advanced.py", "Agente avanzado"),
        ("agent/agent_api.py", "API REST"),
    ]
    
    for file_path, desc in critical_files:
        if not check_file(file_path, desc):
            all_ok = False
    
    # 2. Verificar dependencias Python
    print_header("2️⃣  DEPENDENCIAS PYTHON")
    
    packages = [
        ("torch", "torch"),
        ("sentence_transformers", "sentence-transformers"),
        ("sklearn", "scikit-learn"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
    ]
    
    for import_name, display_name in packages:
        if not check_python_package(display_name, import_name):
            all_ok = False
    
    # 3. Verificar que el modelo puede cargarse
    print_header("3️⃣  VERIFICACIÓN DEL MODELO")
    
    try:
        from loader import load_model
        print("✅ loader.py importado correctamente")
        
        if Path("model/model.safetensors").exists():
            print("⏳ Cargando modelo (esto puede tomar 30 segundos)...")
            model = load_model("./model")
            print(f"✅ Modelo cargado: paraphrase-multilingual-mpnet-base-v2")
            
            # Test rápido
            print("⏳ Test rápido de inferencia...")
            embedding = model.encode("test")
            print(f"✅ Embedding generado: {len(embedding)} dimensiones")
        else:
            print("❌ model.safetensors no encontrado - revisar Git LFS")
            all_ok = False
            
    except Exception as e:
        print(f"❌ Error al cargar modelo: {str(e)}")
        all_ok = False
    
    # 4. Verificar agentes
    print_header("4️⃣  VERIFICACIÓN DE AGENTES")
    
    try:
        from agent.agents_simple import SimpleRecruitmentAgent
        print("✅ SimpleRecruitmentAgent importado")
        
        from agent.agents_advanced import AdvancedRecruitmentAgent
        print("✅ AdvancedRecruitmentAgent importado")
        
        print("✅ Agentes listos para usar")
    except Exception as e:
        print(f"❌ Error al importar agentes: {str(e)}")
        all_ok = False
    
    # 5. Verificar API
    print_header("5️⃣  VERIFICACIÓN DE API")
    
    try:
        from agent.agent_api import app
        print("✅ FastAPI app importada correctamente")
        print("✅ API lista para iniciar: uvicorn agent.agent_api:app --reload")
    except Exception as e:
        print(f"❌ Error al importar API: {str(e)}")
        all_ok = False
    
    # Resultado final
    print_header("RESULTADO FINAL")
    
    if all_ok:
        print("""
        ✅ TODO VERIFICADO - PROYECTO LISTO PARA USAR
        
        PRÓXIMOS PASOS:
        
        1️⃣  Opción A - Agente Simple:
            python agent/agents_simple.py
        
        2️⃣  Opción B - API REST:
            uvicorn agent.agent_api:app --reload --port 8000
            # Acceder a: http://localhost:8000/docs
        
        3️⃣  Opción C - Docker:
            docker build -t recruitment-model .
            docker run -p 8000:8000 recruitment-model
        
        📚 Más documentación:
            - README.md
            - QUICKSTART.md
            - agent/README.md
            - docs/ARCHITECTURE.md
        """)
        return 0
    else:
        print("""
        ⚠️  PROBLEMAS ENCONTRADOS
        
        Soluciones:
        1. Ejecutar: pip install -r requirements.txt
        2. Verificar que Git LFS está instalado: git lfs version
        3. Para descargar modelo con LFS: git lfs pull
        4. Revisar: https://git-lfs.com/ para instalar Git LFS
        """)
        return 1

if __name__ == "__main__":
    sys.exit(main())
