"""FAISS vector store for efficient similarity search."""

import os
import pickle
from typing import List, Tuple
import numpy as np
import faiss
from pathlib import Path


class FAISSVectorStore:
    """Vector store using FAISS for similarity search."""
    
    def __init__(self, embedding_dim: int, index_path: str = "data/processed/faiss_index"):
        """
        Initialize FAISS vector store.
        
        Args:
            embedding_dim: Dimension of the embeddings
            index_path: Path to save/load the index
        """
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.index = None
        self.texts = []
        self.metadatas = []
        
        # Create index directory if it doesn't exist
        Path(index_path).parent.mkdir(parents=True, exist_ok=True)
    
    def create_index(self):
        """Create a new FAISS index."""
        # Using L2 distance (can be changed to inner product for cosine similarity)
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        print(f"Created new FAISS index with dimension {self.embedding_dim}")
    
    def add_embeddings(self, embeddings: np.ndarray, texts: List[str], metadatas: List[dict] = None):
        """
        Add embeddings to the index.
        
        Args:
            embeddings: numpy array of embeddings
            texts: List of corresponding text chunks
            metadatas: List of metadata dictionaries
        """
        if self.index is None:
            self.create_index()
        
        # Ensure embeddings are float32
        embeddings = embeddings.astype('float32')
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to index
        self.index.add(embeddings)
        
        # Store texts and metadata
        self.texts.extend(texts)
        if metadatas:
            self.metadatas.extend(metadatas)
        else:
            self.metadatas.extend([{}] * len(texts))
        
        print(f"Added {len(texts)} embeddings to index. Total: {self.index.ntotal}")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float, dict]]:
        """
        Search for similar embeddings.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
        
        Returns:
            List of tuples (text, score, metadata)
        """
        if self.index is None or self.index.ntotal == 0:
            print("Warning: Index is empty")
            return []
        
        # Ensure query is float32 and 2D
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        
        # Normalize query for cosine similarity
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
        
        # Prepare results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.texts):  # Valid index
                # Convert L2 distance to similarity score (0-1, higher is better)
                similarity = 1 / (1 + dist)
                results.append((
                    self.texts[idx],
                    float(similarity),
                    self.metadatas[idx]
                ))
        
        return results
    
    def save(self):
        """Save the index and metadata to disk."""
        if self.index is None:
            print("Warning: No index to save")
            return
        
        # Save FAISS index
        faiss.write_index(self.index, f"{self.index_path}.faiss")
        
        # Save texts and metadata
        with open(f"{self.index_path}_data.pkl", 'wb') as f:
            pickle.dump({
                'texts': self.texts,
                'metadatas': self.metadatas,
                'embedding_dim': self.embedding_dim
            }, f)
        
        print(f"Saved index to {self.index_path}")
    
    def load(self):
        """Load the index and metadata from disk."""
        index_file = f"{self.index_path}.faiss"
        data_file = f"{self.index_path}_data.pkl"
        
        if not os.path.exists(index_file) or not os.path.exists(data_file):
            print(f"Warning: Index files not found at {self.index_path}")
            return False
        
        # Load FAISS index
        self.index = faiss.read_index(index_file)
        
        # Load texts and metadata
        with open(data_file, 'rb') as f:
            data = pickle.load(f)
            self.texts = data['texts']
            self.metadatas = data['metadatas']
            self.embedding_dim = data['embedding_dim']
        
        print(f"Loaded index with {self.index.ntotal} vectors")
        return True
    
    def clear(self):
        """Clear the index."""
        self.index = None
        self.texts = []
        self.metadatas = []
        print("Cleared index")
