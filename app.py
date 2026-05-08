"""Streamlit web interface for the RAG System."""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from src.rag_system import RAGSystem
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #145a8c;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .doc-source {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
    st.session_state.initialized = False
    st.session_state.query_history = []

def initialize_rag_system():
    """Initialize the RAG system."""
    try:
        with st.spinner("🔄 Initializing RAG System..."):
            rag = RAGSystem()
            st.session_state.rag_system = rag
            st.session_state.initialized = True
            return True
    except Exception as e:
        st.error(f"❌ Error initializing RAG system: {e}")
        return False

def main():
    """Main application."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 RAG System</h1>', unsafe_allow_html=True)
    st.markdown("### Retrieval-Augmented Generation for Intelligent Q&A")
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=100)
        st.title("⚙️ Settings")
        
        # Initialize button
        if not st.session_state.initialized:
            if st.button("🚀 Initialize System", use_container_width=True):
                if initialize_rag_system():
                    st.success("✅ System initialized!")
                    st.rerun()
        else:
            st.success("✅ System Ready")
        
        st.divider()
        
        # Document upload section
        st.subheader("📄 Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload documents (PDF, TXT, DOCX)",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            help="Upload documents to add to the knowledge base"
        )
        
        if uploaded_files and st.button("📥 Add Documents", use_container_width=True):
            if st.session_state.initialized:
                add_documents(uploaded_files)
            else:
                st.warning("⚠️ Please initialize the system first")
        
        st.divider()
        
        # System statistics
        if st.session_state.initialized:
            st.subheader("📊 System Stats")
            stats = st.session_state.rag_system.get_stats()
            st.metric("Total Documents", stats['total_documents'])
            st.metric("Embedding Dimension", stats['embedding_dimension'])
            st.metric("Chunk Size", stats['chunk_size'])
            
            with st.expander("🔧 Advanced Settings"):
                st.text(f"Model: {stats['embedding_model']}")
                st.text(f"LLM: {stats['llm_model']}")
        
        st.divider()
        
        # Clear history
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.query_history = []
            st.rerun()
    
    # Main content area
    if not st.session_state.initialized:
        st.info("👈 Please initialize the system using the sidebar")
        
        # Show features
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 📚 Document Processing")
            st.write("Upload and process PDF, TXT, and DOCX files")
        with col2:
            st.markdown("### 🔍 Semantic Search")
            st.write("Find relevant information using AI-powered search")
        with col3:
            st.markdown("### 💬 Smart Answers")
            st.write("Get intelligent answers from your documents")
        
        return
    
    # Query interface
    st.subheader("💬 Ask a Question")
    
    # Query input
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Enter your question:",
            placeholder="e.g., What is machine learning?",
            label_visibility="collapsed"
        )
    with col2:
        top_k = st.number_input("Top K", min_value=1, max_value=10, value=3, help="Number of documents to retrieve")
    
    # Search button
    if st.button("🔍 Search", use_container_width=True, type="primary"):
        if query:
            process_query(query, top_k)
        else:
            st.warning("⚠️ Please enter a question")
    
    # Display results
    if st.session_state.query_history:
        st.divider()
        st.subheader("📋 Results")
        
        # Show latest result
        latest = st.session_state.query_history[-1]
        
        # Query
        st.markdown(f"**Question:** {latest['query']}")
        
        # Answer
        st.markdown("**Answer:**")
        st.markdown(f'<div class="result-box">{latest["answer"]}</div>', unsafe_allow_html=True)
        
        # Retrieved documents
        if latest['sources']:
            with st.expander(f"📚 View {len(latest['sources'])} Retrieved Documents"):
                for i, source in enumerate(latest['sources'], 1):
                    st.markdown(f"""
                    <div class="doc-source">
                        <strong>Document {i}</strong> - {source['filename']} 
                        <span style="color: #1f77b4;">(Score: {source['score']:.3f})</span>
                        <p style="margin-top: 0.5rem;">{source['text'][:300]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Query history
    if len(st.session_state.query_history) > 1:
        st.divider()
        with st.expander(f"📜 Query History ({len(st.session_state.query_history)} queries)"):
            for i, item in enumerate(reversed(st.session_state.query_history[:-1]), 1):
                st.markdown(f"**{i}. {item['query']}**")
                st.text(f"Time: {item['timestamp']}")
                st.divider()

def add_documents(uploaded_files):
    """Add uploaded documents to the RAG system."""
    try:
        # Save uploaded files temporarily
        temp_dir = Path("data/temp")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        for uploaded_file in uploaded_files:
            file_path = temp_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            saved_files.append(file_path)
        
        # Add to RAG system
        with st.spinner(f"📥 Processing {len(uploaded_files)} document(s)..."):
            st.session_state.rag_system.add_documents(str(temp_dir))
        
        # Clean up
        for file_path in saved_files:
            file_path.unlink()
        
        st.success(f"✅ Successfully added {len(uploaded_files)} document(s)!")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error adding documents: {e}")

def process_query(query, top_k):
    """Process a user query."""
    try:
        with st.spinner("🔍 Searching and generating answer..."):
            # Get retrieval results
            results = st.session_state.rag_system.retriever.retrieve(query, top_k=top_k)
            
            if not results:
                st.warning("⚠️ No relevant documents found")
                return
            
            # Generate answer
            answer = st.session_state.rag_system.generator.generate_with_results(query, results)
            
            # Store in history
            st.session_state.query_history.append({
                'query': query,
                'answer': answer,
                'sources': [
                    {
                        'text': r.text,
                        'score': r.score,
                        'filename': r.metadata.get('filename', 'unknown')
                    }
                    for r in results
                ],
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error processing query: {e}")

if __name__ == "__main__":
    main()
