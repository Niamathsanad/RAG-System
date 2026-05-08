"""Main entry point for the RAG system."""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

from src.rag_system import RAGSystem


def main():
    """Main function."""
    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Foundational RAG System")
    parser.add_argument('--add-docs', type=str, help='Path to documents to add')
    parser.add_argument('--query', type=str, help='Query to ask')
    parser.add_argument('--clear', action='store_true', help='Clear the index')
    parser.add_argument('--stats', action='store_true', help='Show system statistics')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--config', type=str, default='config/config.yaml', help='Path to config file')
    
    args = parser.parse_args()
    
    # Initialize RAG system
    try:
        rag = RAGSystem(config_path=args.config)
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        return
    
    # Handle commands
    if args.add_docs:
        try:
            rag.add_documents(args.add_docs)
        except Exception as e:
            print(f"Error adding documents: {e}")
    
    elif args.query:
        try:
            rag.query(args.query)
        except Exception as e:
            print(f"Error processing query: {e}")
    
    elif args.clear:
        rag.clear_index()
    
    elif args.stats:
        stats = rag.get_stats()
        print("\n" + "="*60)
        print("RAG SYSTEM STATISTICS")
        print("="*60)
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("="*60 + "\n")
    
    elif args.interactive:
        interactive_mode(rag)
    
    else:
        parser.print_help()


def interactive_mode(rag: RAGSystem):
    """Run RAG system in interactive mode."""
    print("\n" + "="*60)
    print("INTERACTIVE RAG SYSTEM")
    print("="*60)
    print("\nCommands:")
    print("  - Type your question to query the system")
    print("  - 'add <path>' to add documents")
    print("  - 'stats' to show statistics")
    print("  - 'clear' to clear the index")
    print("  - 'quit' or 'exit' to exit")
    print("\n" + "="*60 + "\n")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            elif user_input.lower() == 'stats':
                stats = rag.get_stats()
                print("\nSystem Statistics:")
                for key, value in stats.items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            
            elif user_input.lower() == 'clear':
                rag.clear_index()
            
            elif user_input.lower().startswith('add '):
                path = user_input[4:].strip()
                rag.add_documents(path)
            
            else:
                # Treat as query
                rag.query(user_input)
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
