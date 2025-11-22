"""
Agent Usage Examples
Demonstrates how to use each agent in the backend services
"""

import asyncio
from app.agents import (
    ingestion_agent,
    clause_agent,
    compliance_agent,
    risk_agent,
    merge_agent
)


async def example_drafting_service():
    """
    Example: Contract Drafting Service
    Uses only ingestion_agent to normalize input data
    """
    print("\n=== CONTRACT DRAFTING SERVICE EXAMPLE ===\n")
    
    # Sample input from frontend
    input_data = {
        "party_a": "Acme Corporation",
        "party_b": "Example Industries Inc.",
        "jurisdiction": "us",
        "purpose": "Service Agreement",
        "term": "24",
        "contract_type": "service"
    }
    
    # Step 1: Normalize input data
    print("Step 1: Normalizing input data...")
    normalized = await ingestion_agent.run(input_data)
    
    print(f"Extracted metadata:")
    print(f"  Parties: {normalized['meta']['parties']}")
    print(f"  Jurisdiction: {normalized['meta']['jurisdiction']}")
    print(f"  Purpose: {normalized['meta']['purpose']}")
    print(f"  Term: {normalized['meta']['term']}")
    
    # Step 2: Use LLM to draft contract (not shown - would be in llms/ module)
    # drafted_contract = await llm_client.generate(prompt_with_metadata)
    
    # Step 3: Return response
    response = {
        "drafted_contract": "[LLM-generated contract would be here]",
        "compliance_report": []  # Empty for drafting service
    }
    
    print(f"\nDrafting service complete!")
    return response


async def example_compliance_service():
    """
    Example: Compliance Check Service
    Uses clause_agent, compliance_agent, risk_agent, and merge_agent
    """
    print("\n=== COMPLIANCE CHECK SERVICE EXAMPLE ===\n")
    
    # Sample contract text from frontend
    contract_text = """
    TERMINATION CLAUSE
    
    Either party may terminate this agreement with 15 days notice.
    Upon termination, all obligations cease immediately.
    
    LIMITATION OF LIABILITY
    
    The company shall not be liable for any damages whatsoever.
    This includes all direct, indirect, and consequential damages.
    """
    
    # Step 1: Split contract into clauses
    print("Step 1: Extracting clauses from contract...")
    clause_result = await clause_agent.run(contract_text)
    clauses = clause_result["clauses"]
    print(f"Extracted {len(clauses)} clauses\n")
    
    # Step 2-5: Process each clause
    compliance_report = []
    
    for i, clause in enumerate(clauses, 1):
        print(f"Processing clause {i}/{len(clauses)}...")
        
        # Step 2: Perform compliance analysis
        # Note: In production, pass an actual LLM client
        compliance_result = await compliance_agent.run(
            clause=clause,
            jurisdiction="United States",
            llm_client=None  # Will use mock mode
        )
        
        # Step 3: Classify risk level
        risk_result = await risk_agent.run(compliance_result["parsed"])
        
        print(f"  Risk Level: {risk_result['risk_level']}")
        print(f"  Fix: {risk_result['fix'][:50]}...")
        
        # Step 4: Optional - merge clause with fix
        merge_result = await merge_agent.run(clause, risk_result)
        
        # Add to report
        compliance_report.append({
            "clause": clause,
            "risk_level": risk_result["risk_level"],
            "fix": risk_result["fix"],
            "citations": risk_result["citations"]
        })
    
    # Step 6: Build final response
    response = {
        "drafted_contract": contract_text,
        "compliance_report": compliance_report
    }
    
    print(f"\nCompliance check complete!")
    print(f"Total issues found: {len(compliance_report)}")
    return response


async def example_full_workflow():
    """
    Example: Complete workflow demonstration
    """
    print("\n" + "=" * 70)
    print("LEGALCONTRACTAI BACKEND AGENT WORKFLOW DEMONSTRATION")
    print("=" * 70)
    
    # Run drafting service example
    await example_drafting_service()
    
    # Run compliance service example
    await example_compliance_service()
    
    print("\n" + "=" * 70)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(example_full_workflow())
