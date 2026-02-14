import sys
import os

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import (
    INDEX_STATUTES, 
    INDEX_REGULATIONS, 
    INDEX_CLAUSES, 
    INDEX_CASES
)
from app.RAG.pinecone_store import pinecone_service
import time

def setup_indexes():
    indexes = [
        INDEX_STATUTES,
        INDEX_REGULATIONS,
        INDEX_CLAUSES,
        INDEX_CASES
    ]

    print("Checking and creating Pinecone indexes...")
    
    for index_name in indexes:
        try:
            print(f"Processing index: {index_name}")
            # get_index method in pinecone_service handles creation if not exists
            pinecone_service.get_index(index_name)
            print(f"✅ Index '{index_name}' is ready.")
        except Exception as e:
            print(f"❌ Error creating index '{index_name}': {e}")

    print("\nAll indexes have been processed.")

if __name__ == "__main__":
    setup_indexes()
