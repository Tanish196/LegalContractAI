import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd()))

from app.services.supabase_service import db_service

def check_columns():
    if not db_service.client:
        print("Supabase client not initialized.")
        return

    try:
        # Fetch one row to see columns
        response = db_service.client.table("chat_messages").select("*").limit(1).execute()
        if response.data:
            print("Columns found:", response.data[0].keys())
        else:
            print("Table is empty, trying to insert a dummy row...")
            test_data = {"user_id": None, "content": "test"} # Try without user_id first if it fails? No, let's try to get schema.
            # In Supabase/PostgREST, we can't easily get schema without SQL.
            # But we can try to insert and see the error.
            try:
                db_service.client.table("chat_messages").insert({"non_existent_col": "val"}).execute()
            except Exception as e:
                print(f"Insert error (expected): {e}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_columns()
