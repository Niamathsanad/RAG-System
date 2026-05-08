# 🚀 Quick Start Guide

## Running the Web Interface

### ✅ The app is now running!

**Access the web interface at:**
- **Local:** http://localhost:8501
- **Network:** http://192.168.1.6:8501

### 🎯 How to Use

1. **Initialize the System**
   - Click "🚀 Initialize System" in the sidebar
   - Wait for the system to load (downloads embedding model on first run)

2. **Upload Documents** (Optional)
   - Use the file uploader in the sidebar
   - Supports PDF, TXT, and DOCX files
   - Click "📥 Add Documents" to process them

3. **Ask Questions**
   - Type your question in the main input box
   - Adjust "Top K" to control how many documents to retrieve
   - Click "🔍 Search" to get answers

4. **View Results**
   - See the AI-generated answer (or retrieved context)
   - Expand "📚 View Retrieved Documents" to see sources
   - Check "📜 Query History" for previous queries

### 📊 Features

- ✅ **Real-time Search** - Instant semantic search
- ✅ **Document Upload** - Add documents on the fly
- ✅ **Query History** - Track all your questions
- ✅ **Source Attribution** - See where answers come from
- ✅ **System Stats** - Monitor document count and settings

### 🔑 Enable AI Answers

Currently showing retrieved context. To enable AI-generated answers:

1. Create a `.env` file in the project root
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
3. Restart the app

### 🛑 Stop the App

Press `Ctrl+C` in the terminal or close the terminal window.

---

## Alternative: CLI Interface

If you prefer command-line:

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Query
python main.py --query "What is machine learning?"

# Interactive mode
python main.py --interactive

# Show stats
python main.py --stats
```

---

## Next Steps

- 📖 Read [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment options
- 🐳 Try Docker: `docker-compose up -d`
- 🔧 Customize settings in `config/config.yaml`
- 📚 Add more documents to `data/raw/`

---

**Need help?** Check the [README.md](README.md) for full documentation.
