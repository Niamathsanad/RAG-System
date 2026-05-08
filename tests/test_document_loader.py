"""Tests for document loader."""

import pytest
from pathlib import Path
from src.ingestion.document_loader import DocumentLoader, Document


def test_document_creation():
    """Test Document class."""
    doc = Document(content="Test content", metadata={"source": "test.txt"})
    assert doc.content == "Test content"
    assert doc.metadata["source"] == "test.txt"


def test_document_loader_initialization():
    """Test DocumentLoader initialization."""
    loader = DocumentLoader()
    assert loader.encoding == 'utf-8'
    assert '.txt' in loader.SUPPORTED_FORMATS


def test_load_txt_file():
    """Test loading a text file."""
    loader = DocumentLoader()
    
    # Use the sample document
    doc = loader.load_file("data/raw/sample_document.txt")
    
    assert isinstance(doc, Document)
    assert len(doc.content) > 0
    assert doc.metadata['extension'] == '.txt'
    assert 'Machine Learning' in doc.content


def test_unsupported_format():
    """Test loading unsupported file format."""
    loader = DocumentLoader()
    
    with pytest.raises(ValueError):
        loader.load_file("test.xyz")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
