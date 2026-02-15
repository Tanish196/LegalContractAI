import logging
import base64
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            logger.warning("Supabase URL or Key missing. Database operations will fail.")
            self.client = None
        else:
            try:
                self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                self.client = None

    def store_chat_message(self, user_id, content: str = None, encrypted_data: dict = None):
        """
        Stores a chat message. If encrypted_data is provided, it stores only that.
        """
        if not self.client:
            logger.error("Supabase client not initialized.")
            return None

        try:
            data = {
                "user_id": user_id,
            }
            
            if encrypted_data:
                # Use hex encoding for BYTEA column in Supabase/PostgREST
                raw_bytes = encrypted_data["encrypted_content"]
                hex_content = "\\x" + raw_bytes.hex()
                data.update({
                    "encrypted_content": hex_content,
                    "encryption_version": encrypted_data["encryption_version"],
                    "is_encrypted": encrypted_data["is_encrypted"],
                    "content": None
                })
            else:
                data.update({
                    "content": content,
                    "is_encrypted": False
                })

            response = self.client.table("chat_messages").insert(data).execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to store chat message: {e}")
            return None

    def get_chat_history(self, user_id, limit: int = 50):
        """
        Retrieves chat history for a user.
        """
        if not self.client:
            logger.error("Supabase client not initialized.")
            return []

        try:
            response = self.client.table("chat_messages") \
                .select("*") \
                .eq("user_id", user_id) \
                .order("created_at", desc=False) \
                .limit(limit) \
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to fetch chat history: {e}")
            return []

def base64_if_needed(data):
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')
    return data

import base64 # Import inside or move to top

# Singleton instance
db_service = SupabaseService()
