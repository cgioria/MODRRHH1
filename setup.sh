#!/usr/bin/env bash
# Script de Setup Automático - POSIX (Linux/Mac)
# Ejecutar: bash setup.sh

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     SETUP AUTOMÁTICO - RECRUITMENT MODEL                   ║"
echo "║     Este script configura todo automáticamente              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instalar desde https://www.python.org/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION encontrado"

# Crear venv si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment creado"
fi

# Activar venv
echo "⚙️  Activando virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activado"

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencias instaladas"

# Verificar Git LFS
echo "🔍 Verificando Git LFS..."
if command -v git-lfs &> /dev/null; then
    echo "✅ Git LFS instalado"
    echo "📥 Descargando archivos grandes..."
    git lfs pull
else
    echo "⚠️  Git LFS no instalado"
    echo "   Instalar desde: https://git-lfs.com/"
    echo "   O ejecutar: brew install git-lfs (macOS) / apt install git-lfs (Linux)"
fi

# Test de setup
echo ""
echo "🧪 Ejecutando test de setup..."
python setup_check.py

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     ✅ SETUP COMPLETADO - PROYECTO LISTO                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Próximos pasos:"
echo "1. Agente Simple:   python agent/agents_simple.py"
echo "2. API REST:        uvicorn agent.agent_api:app --reload"
echo "3. Docker:          docker build -t recruitment-model ."
echo ""
