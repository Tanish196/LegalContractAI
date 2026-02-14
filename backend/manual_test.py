import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_research():
    print("\n--- Testing Legal Research API ---")
    url = f"{BASE_URL}/api/research/legal-research"
    payload = {
        "query": "What are the penalties for data breach under the DPDP Act 2023?",
        "jurisdiction": "India"
    }
    try:
        start = time.time()
        response = requests.post(url, json=payload)
        duration = time.time() - start
        if response.status_code == 200:
            print(f"✅ Success ({duration:.2f}s)")
            data = response.json()
            print(f"Answer: {data.get('answer')[:100]}...")
            print(f"Citations: {len(data.get('citations', []))}")
        else:
            print(f"❌ Failed ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_chat():
    print("\n--- Testing Chat Assistant API ---")
    url = f"{BASE_URL}/api/chat/chat-assistant"
    payload = {
        "message": "I need help drafting a generic NDA."
    }
    try:
        start = time.time()
        response = requests.post(url, json=payload)
        duration = time.time() - start
        if response.status_code == 200:
            print(f"✅ Success ({duration:.2f}s)")
            data = response.json()
            print(f"Reply: {data.get('reply')[:100]}...")
            print(f"Intent: {data.get('intent')}")
            print(f"Action: {data.get('suggested_action')}")
        else:
            print(f"❌ Failed ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_compliance():
    print("\n--- Testing Compliance Check API ---")
    url = f"{BASE_URL}/api/compliance/check"
    payload = {
        "contract_text": "This agreement shall be governed by the laws of Mars. Term is infinite.",
        "jurisdiction": "India",
        "standards": ["Indian Contract Act"]
    }
    try:
        start = time.time()
        response = requests.post(url, json=payload)
        duration = time.time() - start
        if response.status_code == 200:
            print(f"✅ Success ({duration:.2f}s)")
            data = response.json()
            print(f"Risk Score: {data.get('risk_score')}")
            print(f"Issues: {len(data.get('compliance_issues', []))}")
        else:
            print(f"❌ Failed ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_drafting():
    print("\n--- Testing Contract Drafting API ---")
    url = f"{BASE_URL}/api/drafting/draft"
    payload = {
        "requirements": "Create a simple employment agreement for a software engineer.",
        "purpose": "Employment",
        "jurisdiction": "India",
        "parties": [
            {"name": "Tech Corp", "role": "Employer"},
            {"name": "John Doe", "role": "Employee"}
        ]
    }
    try:
        start = time.time()
        response = requests.post(url, json=payload)
        duration = time.time() - start
        if response.status_code == 200:
            print(f"✅ Success ({duration:.2f}s)")
            data = response.json()
            print(f"Draft Length: {len(data.get('draft_text', ''))} chars")
        else:
            print(f"❌ Failed ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Starting Manual API Tests...")
    # Health Check (implied if root endpoint exists, otherwise skipping)
    
    test_research()
    test_chat()
    test_compliance()
    test_drafting()
    print("\nTests Completed.")
