"""Retrieval module for finding relevant documents."""

from typing import List, Tuple
from ..embeddings.embedding_generator import EmbeddingGenerator
from ..vectorstore.faiss_store import FAISSVectorStore


class RetrievalResult:
    """Represents a retrieval result."""
    
    def __init__(self, text: str, score: float, metadata: dict):
        self.text = text
        self.score = score
        self.metadata = metadata
    
    def __repr__(self):
        return f"RetrievalResult(score={self.score:.3f}, source={self.metadata.get('source', 'unknown')})"


class Retriever:
    """Retrieve relevant documents based on query."""
    
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: FAISSVectorStore):
        """
        Initialize retriever.
        
        Args:
            embedding_generator: Embedding generator instance
            vector_store: Vector store instance
        """
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
    
    def retrieve(self, query: str, top_k: int = 3, score_threshold: float = 0.0) -> List[RetrievalResult]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Query string
            top_k: Number of results to return
            score_threshold: Minimum similarity score threshold
        
        Returns:
            List of RetrievalResult objects
        """
        # Generate query embedding
        query_embedding = self.embedding_generator.embed_text(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        # Filter by threshold and convert to RetrievalResult
        filtered_results = []
        for text, score, metadata in results:
            if score >= score_threshold:
                filtered_results.append(RetrievalResult(text, score, metadata))
        
        return filtered_results
    
    def retrieve_with_context(self, query: str, top_k: int = 3) -> str:
        """
        Retrieve documents and format as context string.
        
        Args:
            query: Query string
            top_k: Number of results to return
        
        Returns:
            Formatted context string
        """
        results = self.retrieve(query, top_k=top_k)
        
        if not results:
            return "No relevant documents found."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            source = result.metadata.get('filename', 'unknown')
            context_parts.append(f"[Document {i} - {source}]\n{result.text}\n")
        
        return "\n".join(context_parts)
