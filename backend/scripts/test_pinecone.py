import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("PINECONE_API_KEY")
if not api_key:
    print("PINECONE_API_KEY not set")
    exit(1)

pc = Pinecone(api_key=api_key)

index_name = "test-index-v2"

# Check if index exists
try:
    existing_indexes = [i.name for i in pc.list_indexes()]
    print(f"Existing indexes: {existing_indexes}")
    
    # Clean up if limit reached
    if len(existing_indexes) >= 5:
         print("Limit reached. Calculating which index to delete...")
         # Try to delete 'indian-statutes' (v1) if it exists, or the test index itself if it exists
         to_delete = "indian-statutes" if "indian-statutes" in existing_indexes else None
         if not to_delete and index_name in existing_indexes:
             to_delete = index_name
         
         if to_delete:
             print(f"Deleting old index {to_delete} to free up space...")
             pc.delete_index(to_delete)
             import time
             time.sleep(5) # Wait for deletion

    existing_indexes = [i.name for i in pc.list_indexes()]
    if index_name not in existing_indexes:
        from pinecone import ServerlessSpec
        print(f"Creating index {index_name}...")
        pc.create_index(
            name=index_name,
            dimension=1024, # multilingual-e5-large
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Index created successfully.")
    else:
        print(f"Index {index_name} already exists.")
except Exception as e:
    print(f"Error: {e}")
