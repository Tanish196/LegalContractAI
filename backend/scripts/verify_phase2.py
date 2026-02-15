import os
import uuid
import base64
import requests
from app.services.encryption import encryption_service
from app.services.supabase_service import db_service

API_BASE_URL = "http://localhost:8000"

def verify_phase2():
    test_user_id = str(uuid.uuid4())
    print(f"--- Starting Phase 2 Verification for User: {test_user_id} ---")

    # 1. Test Encrypted Usage Recording
    service_type = "contract_draft"
    prompt_title = "Commercial Lease Agreement"
    prompt_output = "THIS LEASE AGREEMENT (the 'Lease') is made and entered into..."

    print("Step 1: Recording encrypted usage via API...")
    try:
        payload = {
            "user_id": test_user_id,
            "service_type": service_type,
            "prompt_title": prompt_title,
            "prompt_output": prompt_output
        }
        response = requests.post(f"{API_BASE_URL}/api/usage/record", json=payload)
        response.raise_for_status()
        activity_id = response.json().get("id")
        print(f"✓ Recorded successfully. Activity ID: {activity_id}")
    except Exception as e:
        print(f"✗ Failed to record usage: {e}")
        return

    # 2. Verify Database Storage (Raw Check)
    print("\nStep 2: Verifying database storage format...")
    try:
        item = db_service.get_usage_detail(activity_id)
        is_encrypted = item.get("is_encrypted")
        enc_output = item.get("encrypted_output")
        
        print(f"  Is Encrypted: {is_encrypted}")
        print(f"  Encrypted Output (Raw): {enc_output[:30]}...")
        
        assert is_encrypted == True
        assert item.get("prompt_output") == None
    except Exception as e:
        print(f"✗ Database verification failed: {e}")
        return

    # 3. Verify History Retrieval (List)
    print("\nStep 3: Verifying history list retrieval...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/usage/history?user_id={test_user_id}")
        response.raise_for_status()
        history = response.json().get("history", [])
        print(f"✓ Retrieved {len(history)} items.")
        assert len(history) >= 1
        assert history[0]["id"] == activity_id
    except Exception as e:
        print(f"✗ History list retrieval failed: {e}")
        return

    # 4. Verify Detail Retrieval (Decryption)
    print("\nStep 4: Verifying detail retrieval and decryption...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/usage/history/{activity_id}")
        response.raise_for_status()
        detail = response.json()
        decrypted_output = detail.get("prompt_output")
        
        print(f"  Decrypted Output matches original? {decrypted_output == prompt_output}")
        assert decrypted_output == prompt_output
        print("✓ Decryption successful!")
    except Exception as e:
        print(f"✗ Detail retrieval/decryption failed: {e}")
        return

    # 5. Verify Backward Compatibility (Plaintext)
    print("\nStep 5: Verifying backward compatibility for plaintext records...")
    try:
        # Manually insert a plaintext record
        plaintext_output = "I am an old plaintext document."
        db_service.record_usage(
            user_id=test_user_id,
            service_type="compliance_check",
            prompt_title="Legacy Report",
            prompt_output=plaintext_output
        )
        
        # Fetch history and then detail
        response = requests.get(f"{API_BASE_URL}/api/usage/history?user_id={test_user_id}")
        latest_history = response.json()["history"]
        plaintext_id = latest_history[0]["id"] # Recent one
        
        # Get detail
        response = requests.get(f"{API_BASE_URL}/api/usage/history/{plaintext_id}")
        detail = response.json()
        print(f"  Plaintext Output matches? {detail.get('prompt_output') == plaintext_output}")
        assert detail.get('prompt_output') == plaintext_output
        print("✓ Backward compatibility verified!")
    except Exception as e:
        print(f"✗ Backward compatibility verification failed: {e}")
        return

    print(f"\n--- Phase 2 Verification COMPLETE for User: {test_user_id} ---")

if __name__ == "__main__":
    verify_phase2()
