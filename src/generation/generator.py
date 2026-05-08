"""Generation module for LLM-based answer generation."""

import os
from typing import List, Optional
from ..retrieval.retriever import RetrievalResult


class Generator:
    """Generate answers using LLM with retrieved context."""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-3.5-turbo", 
                 temperature: float = 0.7, max_tokens: int = 500):
        """
        Initialize generator.
        
        Args:
            provider: LLM provider ('openai', 'anthropic', or 'local')
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        """
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the LLM client based on provider."""
        if self.provider == "openai":
            try:
                from openai import OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    print("Warning: OPENAI_API_KEY not found in environment")
                    return
                self.client = OpenAI(api_key=api_key)
                print(f"Initialized OpenAI client with model: {self.model}")
            except ImportError:
                print("Error: openai package not installed")
        
        elif self.provider == "anthropic":
            try:
                from anthropic import Anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    print("Warning: ANTHROPIC_API_KEY not found in environment")
                    return
                self.client = Anthropic(api_key=api_key)
                print(f"Initialized Anthropic client with model: {self.model}")
            except ImportError:
                print("Error: anthropic package not installed")
        
        else:
            print(f"Warning: Provider '{self.provider}' not implemented")
    
    def generate(self, query: str, context: str) -> str:
        """
        Generate an answer based on query and context.
        
        Args:
            query: User query
            context: Retrieved context
        
        Returns:
            Generated answer
        """
        if self.client is None:
            return self._generate_fallback(query, context)
        
        prompt = self._create_prompt(query, context)
        
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt)
            elif self.provider == "anthropic":
                return self._generate_anthropic(prompt)
            else:
                return self._generate_fallback(query, context)
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._generate_fallback(query, context)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create the prompt for the LLM."""
        return f"""You are a helpful assistant that answers questions based on the provided context.

Context:
{context}

Question: {query}

Instructions:
- Answer the question based on the context provided
- If the context doesn't contain enough information, say so
- Be concise and accurate
- Cite the document source when relevant

Answer:"""
    
    def _generate_openai(self, prompt: str) -> str:
        """Generate using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str) -> str:
        """Generate using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def _generate_fallback(self, query: str, context: str) -> str:
        """Fallback response when LLM is not available."""
        return f"""[LLM not configured - showing retrieved context]

Query: {query}

Retrieved Context:
{context}

Note: To get AI-generated answers, please configure your API key in the .env file."""
    
    def generate_with_results(self, query: str, results: List[RetrievalResult]) -> str:
        """
        Generate answer from retrieval results.
        
        Args:
            query: User query
            results: List of retrieval results
        
        Returns:
            Generated answer
        """
        if not results:
            return "I couldn't find any relevant information to answer your question."
        
        # Format context from results
        context_parts = []
        for i, result in enumerate(results, 1):
            source = result.metadata.get('filename', 'unknown')
            context_parts.append(f"[Document {i} - {source}]\n{result.text}")
        
        context = "\n\n".join(context_parts)
        
        return self.generate(query, context)
