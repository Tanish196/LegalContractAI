import sys
import os
import time

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from app.config import INDEX_STATUTES, INDEX_CASES, INDEX_CLAUSES, INDEX_REGULATIONS
from app.RAG.pinecone_store import pinecone_service

# --- Mock Data Generators ---

def get_mock_statutes():
    """
    Generates mock Indian statutes.
    Strategy: Chunk by section.
    Metadata: statute_name, section, jurisdiction="India".
    """
    return [
        Document(
            page_content="The Personal Data Protection Bill, 2019. Section 3. Definitions. (1) In this Act, unless the context otherwise requires,— (a) “anonymisation” in relation to personal data, means such irreversible process of transforming or converting personal data to a form in which a data principal cannot be identified...",
            metadata={"statute_name": "Personal Data Protection Bill, 2019", "section": "3", "jurisdiction": "India", "category": "Privacy"}
        ),
        Document(
            page_content="The Indian Contract Act, 1872. Section 10. All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void.",
            metadata={"statute_name": "Indian Contract Act, 1872", "section": "10", "jurisdiction": "India", "category": "Contract Law"}
        ),
         Document(
            page_content="The Arbitration and Conciliation Act, 1996. Section 7. Arbitration agreement. (1) In this Part, “arbitration agreement” means an agreement by the parties to submit to arbitration all or certain disputes which have arisen or which may arise between them in respect of a defined legal relationship...",
            metadata={"statute_name": "Arbitration and Conciliation Act, 1996", "section": "7", "jurisdiction": "India", "category": "Arbitration"}
        )
    ]

def get_mock_cases():
    """
    Generates mock Case Law summaries.
    Metadata: title, citation, year, court.
    """
    return [
        Document(
            page_content="Justice K.S. Puttaswamy (Retd.) v. Union of India. The Supreme Court of India held that the right to privacy is a fundamental right protected under Article 21 and Part III of the Constitution of India.",
            metadata={"title": "Puttaswamy v. Union of India", "citation": "(2017) 10 SCC 1", "year": "2017", "court": "Supreme Court of India", "jurisdiction": "India"}
        ),
        Document(
            page_content="Tata Sons Ltd. v. State of West Bengal. The court discussed the parameters of public policy in the context of setting aside an arbitral award.",
            metadata={"title": "Tata Sons Ltd. v. State of West Bengal", "citation": "MANU/SC/0001/2000", "year": "2000", "court": "Supreme Court of India", "jurisdiction": "India"}
        )
    ]

def get_mock_clauses():
    """
    Generates mock Contract Clauses.
    Strategy: One document per clause. No overlap.
    Metadata: clause_type, contract_type, jurisdiction.
    """
    return [
        Document(
            page_content="Confidentiality. The Recipient shall keep the Confidential Information strictly confidential and shall not disclose it to any third party without the prior written consent of the Disclosing Party.",
            metadata={"clause_type": "Confidentiality", "contract_type": "NDA", "jurisdiction": "India"}
        ),
        Document(
            page_content="Governing Law and Jurisdiction. This Agreement shall be governed by and construed in accordance with the laws of India. The courts at New Delhi shall have exclusive jurisdiction.",
            metadata={"clause_type": "Governing Law", "contract_type": "General", "jurisdiction": "India"}
        ),
        Document(
            page_content="Indemnification. The Service Provider agrees to indemnify and hold harmless the Client from any claims, damages, or liabilities arising out of the Service Provider's negligence or breach of this Agreement.",
            metadata={"clause_type": "Indemnification", "contract_type": "Service Agreement", "jurisdiction": "India"}
        ),
        Document(
            page_content="Termination. Either party may terminate this Agreement by giving 30 days written notice to the other party.",
            metadata={"clause_type": "Termination", "contract_type": "General", "jurisdiction": "India"}
        )
    ]

def get_mock_regulations():
    """
    Generates mock Regulations.
    """
    return [
        Document(
             page_content="RBI Guidelines on Outsourcing of Financial Services. Banks cannot outsource core management functions including Internal Audit and Compliance functions.",
             metadata={"regulatory_body": "RBI", "topic": "Outsourcing", "jurisdiction": "India"}
        )
    ]


def ingest_data():
    print("Starting data ingestion with specialized strategies...")
    
    # Clean up old indexes if needed to stay within limits (Limit: 5)
    pc = pinecone_service.pc
    existing_indexes = [i.name for i in pc.list_indexes()]
    print(f"Current indexes: {existing_indexes}")
    
    # List of v1 indexes to cleanup
    v1_indexes = ["indian-statutes", "indian-regulations", "contract-clauses", "case-law-summaries", "test-index-v2"]
    
    for old_index in v1_indexes:
        if old_index in existing_indexes:
            print(f"Removing old index {old_index} to free up space...")
            try:
                pc.delete_index(old_index)
                print(f"Deleted {old_index}")
            except Exception as e:
                print(f"Failed to delete {old_index}: {e}")
                
    # Wait a moment for deletion to propagate
    import time
    time.sleep(5)
    
    # --- 1. Statutes (Chunking: Section based - represented by pre-chunked docs here) ---
    print(f"Ingesting Statutes into {INDEX_STATUTES}...")
    statutes = get_mock_statutes()
    try:
        vector_store = pinecone_service.get_vector_store(INDEX_STATUTES)
        vector_store.add_documents(statutes)
        print(f"✅ Added {len(statutes)} statutes.")
    except Exception as e:
        print(f"❌ Error ingesting statutes: {e}")

    # --- 2. Cases ---
    print(f"Ingesting Cases into {INDEX_CASES}...")
    cases = get_mock_cases()
    try:
        vector_store = pinecone_service.get_vector_store(INDEX_CASES)
        vector_store.add_documents(cases)
        print(f"✅ Added {len(cases)} cases.")
    except Exception as e:
        print(f"❌ Error ingesting cases: {e}")

    # --- 3. Contract Clauses (Chunking: Per Clause) ---
    print(f"Ingesting Clauses into {INDEX_CLAUSES}...")
    clauses = get_mock_clauses()
    try:
        vector_store = pinecone_service.get_vector_store(INDEX_CLAUSES)
        vector_store.add_documents(clauses)
        print(f"✅ Added {len(clauses)} clauses.")
    except Exception as e:
        print(f"❌ Error ingesting clauses: {e}")

    # --- 4. Regulations ---
    print(f"Ingesting Regulations into {INDEX_REGULATIONS}...")
    regulations = get_mock_regulations()
    try:
        vector_store = pinecone_service.get_vector_store(INDEX_REGULATIONS)
        vector_store.add_documents(regulations)
        print(f"✅ Added {len(regulations)} regulations.")
    except Exception as e:
        print(f"❌ Error ingesting regulations: {e}")

    print("\nData ingestion complete.")

if __name__ == "__main__":
    ingest_data()
