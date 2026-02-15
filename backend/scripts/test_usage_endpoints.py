from fastapi.testclient import TestClient
import uuid
import json
from app.main import app
from app.services.supabase_service import db_service
from app.services.encryption import encryption_service

import sys
client = TestClient(app)

def test_usage_encryption():
    # Use a real user ID from auth.users to satisfy FK constraints if present
    test_user_id = "25a6e13e-f9a6-4889-88c0-845f9c4bc2e4"
    print(f"--- Testing Usage Encryption via TestClient for User: {test_user_id} ---")
    sys.stdout.flush()

    # 1. Record Usage
    service_type = "contract_draft"
    prompt_title = "Commercial Lease Agreement"
    prompt_output = "THIS LEASE AGREEMENT (the 'Lease') is made and entered into..."

    print("Step 1: Recording usage...")
    response = client.post("/api/usage/record", json={
        "user_id": test_user_id,
        "service_type": service_type,
        "prompt_title": prompt_title,
        "prompt_output": prompt_output
    })
    
    if response.status_code != 200:
        print(f"ERROR: {response.status_code}")
        print(f"Response Body: {response.text}")
    assert response.status_code == 200
    activity_id = response.json().get("id")
    print(f"OK: Recorded successfully. Activity ID: {activity_id}")

    # 2. Check Database (Manual retrieval through service)
    print("\nStep 2: Checking database...")
    item = db_service.get_usage_detail(activity_id)
    assert item["is_encrypted"] == True
    assert item["prompt_output"] == None
    print("OK: Data found and is encrypted in DB.")

    # 3. Fetch History List
    print("\nStep 3: Fetching history list...")
    response = client.get(f"/api/usage/history?user_id={test_user_id}")
    assert response.status_code == 200
    history = response.json()["history"]
    assert len(history) >= 1
    assert history[0]["id"] == activity_id
    print(f"OK: History list verified (size: {len(history)}).")

    # 4. Fetch Detail (Decryption)
    print("\nStep 4: Fetching detail with decryption...")
    response = client.get(f"/api/usage/history/{activity_id}")
    assert response.status_code == 200
    detail = response.json()
    assert detail["prompt_output"] == prompt_output
    print("OK: Decryption successful!")

    # 5. Backward Compatibility
    print("\nStep 5: Checking backward compatibility...")
    plaintext_msg = "Old plaintext document"
    db_service.record_usage(
        user_id=test_user_id,
        service_type="compliance_check",
        prompt_title="Legacy Doc",
        prompt_output=plaintext_msg
    )
    
    # Get the latest one
    response = client.get(f"/api/usage/history?user_id={test_user_id}")
    history = response.json()["history"]
    plaintext_id = history[0]["id"]
    
    response = client.get(f"/api/usage/history/{plaintext_id}")
    assert response.status_code == 200
    assert response.json()["prompt_output"] == plaintext_msg
    print("OK: Backward compatibility verified!")

    print(f"\n--- TestClient Verification COMPLETE for User: {test_user_id} ---")

if __name__ == "__main__":
    test_usage_encryption()
