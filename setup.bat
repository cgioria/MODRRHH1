@echo off
REM Setup Automático para Windows
REM Ejecutar: setup.bat

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     SETUP AUTOMATICO - RECRUITMENT MODEL                   ║
echo ║     Este script configura todo automaticamente              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Instalar desde https://www.python.org/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% encontrado

REM Crear venv si no existe
if not exist "venv\" (
    echo 📦 Creando virtual environment...
    python -m venv venv
    echo ✅ Virtual environment creado
)

REM Activar venv
echo ⚙️  Activando virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activado

REM Instalar dependencias
echo 📚 Instalando dependencias...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
echo ✅ Dependencias instaladas

REM Verificar Git LFS
echo 🔍 Verificando Git LFS...
git lfs version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Git LFS no instalado
    echo    Descargar desde: https://git-lfs.com/
    echo    O: choco install git-lfs ^(si tienes Chocolatey^)
) else (
    echo ✅ Git LFS instalado
    echo 📥 Descargando archivos grandes...
    git lfs pull
)

REM Test de setup
echo.
echo 🧪 Ejecutando test de setup...
python setup_check.py

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     ✅ SETUP COMPLETADO - PROYECTO LISTO                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Proximos pasos:
echo 1. Agente Simple:   python agent/agents_simple.py
echo 2. API REST:        uvicorn agent.agent_api:app --reload
echo 3. Docker:          docker build -t recruitment-model .
echo.
pause
