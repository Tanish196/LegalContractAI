import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from app.RAG.pinecone_store import pinecone_service
from app.config import INDEX_STATUTES

async def test_rag():
    print(f"Testing RAG retrieval from {INDEX_STATUTES}...")
    try:
        # Get vector store
        vector_store = pinecone_service.get_vector_store(INDEX_STATUTES)
        
        query = "What is the definition of personal data?"
        print(f"Query: {query}")
        
        # Search
        # Note: similarity_search calls Pinecone embeddings (server-side) then queries index
        docs = vector_store.similarity_search(query, k=2)
        
        print(f"\nFound {len(docs)} documents:")
        for i, doc in enumerate(docs):
            print(f"{i+1}. {doc.page_content[:200]}...")
            print(f"   Metadata: {doc.metadata}")
            
    except Exception as e:
        print(f"❌ Error testing RAG: {e}")

if __name__ == "__main__":
    asyncio.run(test_rag())
