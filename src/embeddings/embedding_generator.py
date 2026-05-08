"""Embedding generation module using sentence transformers."""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


class EmbeddingGenerator:
    """Generate embeddings for text using sentence transformers."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        """
        Initialize the embedding generator.
        
        Args:
            model_name: Name of the sentence transformer model
            device: Device to run the model on ('cpu' or 'cuda')
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name, device=device)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.embedding_dim}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_texts(self, texts: List[str], batch_size: int = 32, show_progress: bool = True) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of text strings to embed
            batch_size: Batch size for encoding
            show_progress: Whether to show progress bar
        
        Returns:
            numpy array of embeddings with shape (len(texts), embedding_dim)
        """
        if show_progress:
            print(f"Generating embeddings for {len(texts)} texts...")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings."""
        return self.embedding_dim
