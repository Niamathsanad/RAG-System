@echo off
REM Setup script for RAG System (Windows)

echo 🚀 Setting up RAG System...

REM Check Python version
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo 📁 Creating directories...
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed
if not exist "data\temp" mkdir data\temp

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your API keys
)

echo.
echo ✅ Setup complete!
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run web interface: streamlit run app.py
echo   3. Or run CLI: python main.py --help
echo.
echo To deploy with Docker:
echo   docker-compose up -d
echo.
pause
