"""Main RAG System orchestrator."""

import os
import yaml
from pathlib import Path
from typing import List, Optional

from .ingestion.document_loader import DocumentLoader
from .ingestion.text_splitter import TextSplitter
from .embeddings.embedding_generator import EmbeddingGenerator
from .vectorstore.faiss_store import FAISSVectorStore
from .retrieval.retriever import Retriever
from .generation.generator import Generator


class RAGSystem:
    """Complete RAG system orchestrator."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize RAG system.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        
        # Initialize components
        print("Initializing RAG System...")
        
        # Document processing
        self.document_loader = DocumentLoader(
            encoding=self.config['documents']['encoding']
        )
        
        self.text_splitter = TextSplitter(
            chunk_size=self.config['chunking']['chunk_size'],
            chunk_overlap=self.config['chunking']['chunk_overlap'],
            separator=self.config['chunking']['separator']
        )
        
        # Embeddings
        self.embedding_generator = EmbeddingGenerator(
            model_name=self.config['embeddings']['model_name'],
            device=self.config['embeddings']['device']
        )
        
        # Vector store
        self.vector_store = FAISSVectorStore(
            embedding_dim=self.embedding_generator.get_embedding_dimension(),
            index_path=self.config['vectorstore']['index_path']
        )
        
        # Try to load existing index
        if not self.vector_store.load():
            print("No existing index found. Will create new index when documents are added.")
        
        # Retrieval
        self.retriever = Retriever(
            embedding_generator=self.embedding_generator,
            vector_store=self.vector_store
        )
        
        # Generation
        self.generator = Generator(
            provider=self.config['llm']['provider'],
            model=self.config['llm']['model'],
            temperature=self.config['llm']['temperature'],
            max_tokens=self.config['llm']['max_tokens']
        )
        
        print("RAG System initialized successfully!\n")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def add_documents(self, path: str):
        """
        Add documents to the RAG system.
        
        Args:
            path: Path to file or directory
        """
        print(f"\n{'='*60}")
        print("ADDING DOCUMENTS TO RAG SYSTEM")
        print(f"{'='*60}\n")
        
        # Load documents
        path_obj = Path(path)
        if path_obj.is_file():
            documents = [self.document_loader.load_file(path)]
        elif path_obj.is_dir():
            documents = self.document_loader.load_directory(path)
        else:
            raise ValueError(f"Invalid path: {path}")
        
        if not documents:
            print("No documents found!")
            return
        
        print(f"\nLoaded {len(documents)} document(s)")
        
        # Split into chunks
        print("\nSplitting documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        # Generate embeddings
        print("\nGenerating embeddings...")
        chunk_texts = [chunk.content for chunk in chunks]
        chunk_metadatas = [chunk.metadata for chunk in chunks]
        
        embeddings = self.embedding_generator.embed_texts(
            chunk_texts,
            batch_size=self.config['embeddings']['batch_size']
        )
        
        # Add to vector store
        print("\nAdding to vector store...")
        self.vector_store.add_embeddings(embeddings, chunk_texts, chunk_metadatas)
        
        # Save index
        print("\nSaving index...")
        self.vector_store.save()
        
        print(f"\n{'='*60}")
        print("DOCUMENTS ADDED SUCCESSFULLY!")
        print(f"{'='*60}\n")
    
    def query(self, question: str, top_k: Optional[int] = None) -> str:
        """
        Query the RAG system.
        
        Args:
            question: User question
            top_k: Number of documents to retrieve (uses config default if None)
        
        Returns:
            Generated answer
        """
        if top_k is None:
            top_k = self.config['retrieval']['top_k']
        
        print(f"\n{'='*60}")
        print(f"QUERY: {question}")
        print(f"{'='*60}\n")
        
        # Retrieve relevant documents
        print(f"Retrieving top {top_k} relevant documents...")
        results = self.retriever.retrieve(
            question,
            top_k=top_k,
            score_threshold=self.config['retrieval']['score_threshold']
        )
        
        if not results:
            return "I couldn't find any relevant information to answer your question."
        
        print(f"Found {len(results)} relevant document(s):\n")
        for i, result in enumerate(results, 1):
            source = result.metadata.get('filename', 'unknown')
            print(f"  {i}. {source} (score: {result.score:.3f})")
        
        # Generate answer
        print("\nGenerating answer...\n")
        answer = self.generator.generate_with_results(question, results)
        
        print(f"{'='*60}")
        print("ANSWER:")
        print(f"{'='*60}\n")
        print(answer)
        print(f"\n{'='*60}\n")
        
        return answer
    
    def clear_index(self):
        """Clear the vector store index."""
        self.vector_store.clear()
        print("Index cleared successfully!")
    
    def get_stats(self) -> dict:
        """Get statistics about the RAG system."""
        return {
            'total_documents': self.vector_store.index.ntotal if self.vector_store.index else 0,
            'embedding_model': self.config['embeddings']['model_name'],
            'embedding_dimension': self.embedding_generator.get_embedding_dimension(),
            'chunk_size': self.config['chunking']['chunk_size'],
            'llm_model': self.config['llm']['model']
        }
