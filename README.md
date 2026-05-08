# Foundational RAG System

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/Niamathsanad/RAG-System)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Streamlit%20Cloud-FF4B4B)](https://share.streamlit.io)

A Retrieval-Augmented Generation (RAG) system that combines document retrieval with language model generation for intelligent question answering.

**🌐 GitHub Repository:** https://github.com/Niamathsanad/RAG-System

## 🌟 Features

- **Document Ingestion**: Load and process various document formats (PDF, TXT, DOCX)
- **Text Chunking**: Intelligent text splitting with overlap for better context
- **Vector Embeddings**: Convert text chunks to embeddings using sentence transformers
- **Vector Storage**: Store and retrieve embeddings using FAISS
- **Semantic Search**: Find relevant documents based on query similarity
- **LLM Integration**: Generate answers using retrieved context
- **Web Interface**: Beautiful Streamlit UI for easy interaction
- **CLI Interface**: Command-line tools for automation

## 🚀 Quick Start

### 1. Setup (Windows)

```bash
# Run setup script
setup.bat

# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Web Interface

```bash
streamlit run app.py
```

**Access at:** http://localhost:8501

### 3. Or Use CLI

```bash
# Add documents
python main.py --add-docs data/raw/

# Query
python main.py --query "What is machine learning?"

# Interactive mode
python main.py --interactive
```

## 📁 Project Structure

```
.
├── app.py                 # 🌐 Web interface (Streamlit)
├── main.py               # 💻 CLI interface
├── src/
│   ├── ingestion/        # 📄 Document loading & chunking
│   ├── embeddings/       # 🔢 Embedding generation
│   ├── vectorstore/      # 🗄️ FAISS vector database
│   ├── retrieval/        # 🔍 Document retrieval
│   ├── generation/       # 🤖 LLM answer generation
│   └── rag_system.py     # 🎯 Main orchestrator
├── data/
│   ├── raw/             # 📚 Your documents
│   └── processed/       # 💾 Vector indexes
├── config/              # ⚙️ Configuration files
├── tests/               # 🧪 Unit tests
└── requirements.txt     # 📦 Dependencies
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## ☁️ Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guides:

- **Streamlit Cloud** (Free, easiest)
- **Heroku** (Simple, scalable)
- **AWS EC2** (Full control)
- **Google Cloud Run** (Serverless)
- **Azure** (Enterprise)
- **DigitalOcean** (Developer-friendly)

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
embeddings:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"
  device: "cpu"

chunking:
  chunk_size: 500
  chunk_overlap: 50

retrieval:
  top_k: 3
  score_threshold: 0.5

llm:
  provider: "openai"
  model: "gpt-3.5-turbo"
  temperature: 0.7
```

## 🔑 API Keys

Create a `.env` file:

```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

## 📖 Usage Examples

### Web Interface

1. **Initialize System** - Click button in sidebar
2. **Upload Documents** - Drag & drop files
3. **Ask Questions** - Type and search
4. **View Results** - See answers and sources

### Python API

```python
from src.rag_system import RAGSystem

# Initialize
rag = RAGSystem()

# Add documents
rag.add_documents("data/raw/")

# Query
answer = rag.query("What is machine learning?")
print(answer)
```

### CLI

```bash
# Add documents
python main.py --add-docs data/raw/

# Query
python main.py --query "Your question here"

# Interactive mode
python main.py --interactive

# Show statistics
python main.py --stats

# Clear index
python main.py --clear
```

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Test document loader
python -m pytest tests/test_document_loader.py
```

## 📊 System Requirements

- **Python**: 3.11+
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB for models and data
- **OS**: Windows, Linux, macOS

## 🎯 Performance

- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Vector Store**: FAISS (fast similarity search)
- **Retrieval Speed**: ~50ms per query
- **Supports**: 1000+ documents

## 🔒 Security

- Environment variables for API keys
- No hardcoded credentials
- HTTPS support in production
- Optional authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Issue: Model download fails
**Solution**: Check internet connection, try again

### Issue: Out of memory
**Solution**: Reduce chunk_size in config, use smaller model

### Issue: Slow queries
**Solution**: Use GPU (change device to "cuda"), reduce top_k

### Issue: No results found
**Solution**: Lower score_threshold, add more documents

## 📚 Documentation

- [Quick Start Guide](QUICK_START.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Project Status](PROJECT_STATUS.md)
- [API Documentation](docs/API.md) (coming soon)

## 🌟 Features Roadmap

- [ ] Multi-language support
- [ ] Advanced filtering
- [ ] Query suggestions
- [ ] Document summarization
- [ ] Export results
- [ ] User authentication
- [ ] Analytics dashboard
- [ ] API endpoints

## 💡 Use Cases

- **Knowledge Base**: Company documentation Q&A
- **Research**: Academic paper search
- **Customer Support**: FAQ automation
- **Legal**: Contract analysis
- **Healthcare**: Medical literature search
- **Education**: Study material assistant

## 🎓 Learn More

- [RAG Explained](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [Streamlit Docs](https://docs.streamlit.io/)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/rag-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/rag-system/discussions)
- **Email**: support@example.com

---

**Built with ❤️ using Python, Streamlit, FAISS, and Sentence Transformers**

⭐ Star this repo if you find it useful!
