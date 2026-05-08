"""Example usage of the RAG system."""

from dotenv import load_dotenv
from src.rag_system import RAGSystem

# Load environment variables
load_dotenv()


def main():
    """Example usage."""
    print("="*60)
    print("RAG SYSTEM EXAMPLE")
    print("="*60)
    
    # Initialize RAG system
    print("\n1. Initializing RAG System...")
    rag = RAGSystem()
    
    # Add documents
    print("\n2. Adding sample documents...")
    rag.add_documents("data/raw/")
    
    # Show statistics
    print("\n3. System Statistics:")
    stats = rag.get_stats()
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Query the system
    print("\n4. Querying the system...")
    
    questions = [
        "What is machine learning?",
        "What are the types of machine learning?",
        "What are some applications of machine learning?"
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        answer = rag.query(question)
        print()
    
    print("="*60)
    print("Example completed!")
    print("="*60)


if __name__ == "__main__":
    main()
