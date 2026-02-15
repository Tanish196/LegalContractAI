"""
API Test Script
Quick tests for the backend API endpoints
"""

import asyncio
import json
from pathlib import Path


async def test_health():
    """Test health endpoint"""
    import aiohttp
    
    print("\n" + "=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://localhost:8000/api/health") as response:
                result = await response.json()
                print(f"Status: {response.status}")
                print(f"Response: {json.dumps(result, indent=2)}")
                return response.status == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False


async def test_drafting():
    """Test contract drafting endpoint"""
    import aiohttp
    
    print("\n" + "=" * 60)
    print("TEST 2: Contract Drafting")
    print("=" * 60)
    
    # Load test data
    test_file = Path(__file__).parent / "test_draft.json"
    with open(test_file, 'r') as f:
        data = json.load(f)
    
    print(f"Request: Party A = {data['party_a']}, Party B = {data['party_b']}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "http://localhost:8000/api/drafting/draft",
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                result = await response.json()
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    contract = result.get("drafted_contract", "")
                    print(f"Contract Length: {len(contract)} chars")
                    print(f"Preview: {contract[:200]}...")
                    print(f"Metadata: {json.dumps(result.get('metadata'), indent=2)}")
                    return True
                else:
                    print(f"Error: {json.dumps(result, indent=2)}")
                    return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return False


async def test_compliance():
    """Test compliance check endpoint"""
    import aiohttp
    
    print("\n" + "=" * 60)
    print("TEST 3: Compliance Check")
    print("=" * 60)
    
    # Load test data
    test_file = Path(__file__).parent / "test_compliance.json"
    with open(test_file, 'r') as f:
        data = json.load(f)
    
    print(f"Request: Analyzing contract with {len(data['contract_text'])} chars")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "http://localhost:8000/api/compliance/check",
                json=data,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                result = await response.json()
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    report = result.get("compliance_report", [])
                    summary = result.get("summary", {})
                    
                    print(f"\nCompliance Report:")
                    print(f"  Total Clauses: {summary.get('total_clauses', 0)}")
                    print(f"  High Risk: {summary.get('high_risk', 0)}")
                    print(f"  Medium Risk: {summary.get('medium_risk', 0)}")
                    print(f"  Low Risk: {summary.get('low_risk', 0)}")
                    print(f"  Assessment: {summary.get('overall_assessment', 'N/A')}")
                    
                    print(f"\nIssues Found: {len(report)}")
                    for i, issue in enumerate(report[:3], 1):
                        print(f"\n  Issue {i}:")
                        print(f"    Risk Level: {issue.get('risk_level')}")
                        print(f"    Clause: {issue.get('clause', '')[:80]}...")
                        print(f"    Fix: {issue.get('fix', '')[:100]}...")
                    
                    return True
                else:
                    print(f"Error: {json.dumps(result, indent=2)}")
                    return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return False


async def test_research():
    """Test legal research endpoint"""
    import aiohttp
    
    print("\n" + "=" * 60)
    print("TEST 4: Legal Research")
    print("=" * 60)
    
    data = {
        "query": "What are the requirements for a valid contract in India?",
        "jurisdiction": "India"
    }
    
    print(f"Query: {data['query']}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "http://localhost:8000/api/research/legal-research",
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                result = await response.json()
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    answer = result.get("answer", "")
                    citations = result.get("citations", [])
                    print(f"Answer Length: {len(answer)} chars")
                    print(f"Citations: {len(citations)}")
                    print(f"Preview: {answer[:200]}...")
                    return True
                else:
                    print(f"Error: {json.dumps(result, indent=2)}")
                    return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

async def test_summarization():
    """Test case summarization endpoint"""
    import aiohttp
    
    print("\n" + "=" * 60)
    print("TEST 5: Case Summarization")
    print("=" * 60)
    
    data = {
        "case_text": "This is a sample case text. The court held that the contract was void due to lack of consideration. Section 25 of the Indian Contract Act was cited." * 10
    }
    
    print(f"Case Text Length: {len(data['case_text'])} chars")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "http://localhost:8000/api/summarization/summarize-case",
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                result = await response.json()
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    summary = result.get("summary", "")
                    key_holdings = result.get("key_holdings", [])
                    print(f"Summary Length: {len(summary)} chars")
                    print(f"Key Holdings: {len(key_holdings)}")
                    print(f"Preview: {summary[:200]}...")
                    return True
                else:
                    print(f"Error: {json.dumps(result, indent=2)}")
                    return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

async def test_analysis():
    """Test clause analysis endpoint"""
    import aiohttp
    
    print("\n" + "=" * 60)
    print("TEST 6: Clause Analysis")
    print("=" * 60)
    
    data = {
        "text": "The service provider shall not be liable for any damages, ensuring they have zero responsibility."
    }
    
    print(f"Clause: {data['text']}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "http://localhost:8000/api/analysis/analyze-clauses",
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                result = await response.json()
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    risks = result.get("risks", [])
                    summary = result.get("summary", "")
                    print(f"Risks Found: {len(risks)}")
                    if risks:
                        print(f"  Risk Level: {risks[0].get('risk_level')}")
                        print(f"  Explanation: {risks[0].get('explanation')}")
                    print(f"Summary: {summary[:200]}...")
                    return True
                else:
                    print(f"Error: {json.dumps(result, indent=2)}")
                    return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("LEGALCONTRACTAI API TESTS")
    print("=" * 60)
    print("\nMake sure the server is running:")
    print("  python -m app.main")
    print("\nStarting tests...")
    
    # Run tests
    results = []
    
    # Test 1: Health
    results.append(("Health Check", await test_health()))
    
    # Test 2: Drafting
    results.append(("Contract Drafting", await test_drafting()))
    
    # Test 3: Compliance
    results.append(("Compliance Check", await test_compliance()))

    # Test 4: Research
    results.append(("Legal Research", await test_research()))

    # Test 5: Summarization
    results.append(("Case Summarization", await test_summarization()))

    # Test 6: Analysis
    results.append(("Clause Analysis", await test_analysis()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60 + "\n")
    

if __name__ == "__main__":
    asyncio.run(main())
