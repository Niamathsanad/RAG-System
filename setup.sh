#!/bin/bash

# Setup script for RAG System

echo "🚀 Setting up RAG System..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/raw data/processed data/temp

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run web interface: streamlit run app.py"
echo "  3. Or run CLI: python main.py --help"
echo ""
echo "To deploy with Docker:"
echo "  docker-compose up -d"
echo ""
