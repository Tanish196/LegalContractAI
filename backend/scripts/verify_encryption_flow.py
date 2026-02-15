import sys
import os
import uuid
import base64

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd()))

from app.services.encryption import encryption_service
from app.services.supabase_service import db_service

def verify_flow():
    test_user_id = str(uuid.uuid4())
    print(f"--- Starting Verification for User: {test_user_id} ---")

    # 1. Test Encrypted Message Storage
    plaintext = "This is a highly confidential legal query."
    try:
        encrypted_data = encryption_service.encrypt(plaintext)
        print("✓ Message encrypted successfully.")
        
        db_service.store_chat_message(test_user_id, encrypted_data=encrypted_data)
        print("✓ Encrypted message stored in Supabase.")
    except Exception as e:
        print(f"✗ Failed to store encrypted message: {e}")
        return

    # 2. Test Plaintext Message Storage (Backward Compatibility Scenario)
    plaintext_old = "This is an old plaintext message."
    try:
        db_service.store_chat_message(test_user_id, content=plaintext_old)
        print("✓ Plaintext message stored in Supabase.")
    except Exception as e:
        print(f"✗ Failed to store plaintext message: {e}")

    # 3. Test Retrieval and Decryption
    try:
        history = db_service.get_chat_history(test_user_id)
        print(f"✓ Retrieved {len(history)} messages from history.")
        
        for msg in history:
            is_encrypted = msg.get("is_encrypted")
            raw_content = msg.get("content")
            enc_content_b64 = msg.get("encrypted_content")
            
            if is_encrypted:
                print(f"  [Debug] Raw Encrypted Data: {enc_content_b64[:30]}... (type {type(enc_content_b64)})")
                
                try:
                    if isinstance(enc_content_b64, str):
                        if enc_content_b64.startswith('\\x'):
                            # Postgres hex format
                            encrypted_bytes = bytes.fromhex(enc_content_b64[2:])
                        else:
                            # Try base64
                            encrypted_bytes = base64.b64decode(enc_content_b64)
                    else:
                        encrypted_bytes = bytes(enc_content_b64)
                    
                    decrypted = encryption_service.decrypt(encrypted_bytes)
                    print(f"  [Encrypted] Decrypted: {decrypted}")
                    assert decrypted == plaintext
                except Exception as e:
                    print(f"  ✗ Decryption error: {e}")
                    raise
            else:
                print(f"  [Plaintext] Content: {raw_content}")
                assert raw_content == plaintext_old
                
        print("✓ All messages verified correctly!")
    except Exception as e:
        print(f"✗ Retrieval/Decryption verification failed: {e}")

if __name__ == "__main__":
    verify_flow()
