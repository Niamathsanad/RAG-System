"""Text splitting module for chunking documents."""

from typing import List
from .document_loader import Document


class TextChunk:
    """Represents a chunk of text with metadata."""
    
    def __init__(self, content: str, metadata: dict = None):
        self.content = content
        self.metadata = metadata or {}
    
    def __repr__(self):
        return f"TextChunk(length={len(self.content)})"


class TextSplitter:
    """Split text into chunks with overlap."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50, separator: str = "\n\n"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
    
    def split_document(self, document: Document) -> List[TextChunk]:
        """Split a document into chunks."""
        text = document.content
        chunks = []
        
        # First split by separator
        splits = text.split(self.separator)
        
        current_chunk = ""
        for split in splits:
            # If adding this split would exceed chunk size
            if len(current_chunk) + len(split) > self.chunk_size:
                if current_chunk:
                    # Save current chunk
                    chunk_metadata = document.metadata.copy()
                    chunk_metadata['chunk_index'] = len(chunks)
                    chunks.append(TextChunk(content=current_chunk.strip(), metadata=chunk_metadata))
                    
                    # Start new chunk with overlap
                    overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                    current_chunk = overlap_text + self.separator + split
                else:
                    # Split is too large, need to split it further
                    if len(split) > self.chunk_size:
                        sub_chunks = self._split_large_text(split)
                        for sub_chunk in sub_chunks:
                            chunk_metadata = document.metadata.copy()
                            chunk_metadata['chunk_index'] = len(chunks)
                            chunks.append(TextChunk(content=sub_chunk, metadata=chunk_metadata))
                    else:
                        current_chunk = split
            else:
                # Add to current chunk
                if current_chunk:
                    current_chunk += self.separator + split
                else:
                    current_chunk = split
        
        # Add final chunk
        if current_chunk:
            chunk_metadata = document.metadata.copy()
            chunk_metadata['chunk_index'] = len(chunks)
            chunks.append(TextChunk(content=current_chunk.strip(), metadata=chunk_metadata))
        
        return chunks
    
    def split_documents(self, documents: List[Document]) -> List[TextChunk]:
        """Split multiple documents into chunks."""
        all_chunks = []
        for doc in documents:
            chunks = self.split_document(doc)
            all_chunks.extend(chunks)
        return all_chunks
    
    def _split_large_text(self, text: str) -> List[str]:
        """Split text that's larger than chunk_size."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - self.chunk_overlap
        
        return chunks
