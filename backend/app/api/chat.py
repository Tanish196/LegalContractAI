from fastapi import APIRouter, HTTPException, Query
from app.schemas import ChatRequest, ChatResponse, ErrorResponse, Citation
from app.config import OPENAI_API_KEY, INDEX_STATUTES, INDEX_CASES, INDEX_REGULATIONS
from app.llms import get_llm_client
from app.RAG.pinecone_store import pinecone_service
from app.services.encryption import encryption_service
from app.services.supabase_service import db_service

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
import logging
import json
import base64

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat Assistant"]
)

logger = logging.getLogger(__name__)

# --- Tools Definition ---

@tool
def get_legal_context(query: str):
    """
    Search for Indian legal context, statutes, case laws, and regulations from the knowledge base.
    Use this for any specific legal questions, section queries, or precedent lookups.
    """
    try:
        # Statutes
        statute_store = pinecone_service.get_vector_store(INDEX_STATUTES)
        statute_docs = statute_store.similarity_search(query, k=2)
        
        # Case Law
        case_store = pinecone_service.get_vector_store(INDEX_CASES)
        case_docs = case_store.similarity_search(query, k=2)
        
        context = []
        for doc in statute_docs + case_docs:
            source = doc.metadata.get("source", "Unknown")
            title = doc.metadata.get("title", "Legal Doc")
            context.append({
                "source": source,
                "title": title,
                "content": doc.page_content
            })
        return context
    except Exception as e:
        logger.error(f"RAG Tool Error: {e}")
        return "Failed to retrieve legal context."

@tool
def get_platform_navigation(intent: str):
    """
    Find the URL route for a specific platform tool.
    Input should be the feature name the user is looking for.
    Returns: The route string (e.g., '/contract-drafting')
    """
    routes = {
        "drafting": "/contract-drafting",
        "compliance": "/compliance-check",
        "research": "/legal-research",
        "summarization": "/case-summary",
        "loopholes": "/loophole-detection",
        "classification": "/clause-classification",
    }
    return routes.get(intent.lower(), "null")

@router.post(
    "/chat-assistant",
    response_model=ChatResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Smart Advisory Chat Assistant"
)
async def chat_assistant(request: ChatRequest):
    try:
        user_message = request.message
        user_id = request.user_id
        logger.info(f"Received smart chat message: {user_message} (User: {user_id})")

        # 1. Store original user message if user logged in (encrypted)
        if user_id:
            try:
                enc_user_msg = encryption_service.encrypt(user_message)
                db_service.store_chat_message(user_id, encrypted_data=enc_user_msg)
            except Exception as e:
                logger.error(f"Failed to store encrypted user message: {e}")

        if not OPENAI_API_KEY:
            # Simulation response
            reply = "[Simulation] I am a legal assistant. I can help you draft contracts, check compliance, or research laws."
            if user_id:
                try:
                    enc_reply = encryption_service.encrypt(reply)
                    db_service.store_chat_message(user_id, encrypted_data=enc_reply)
                except Exception as e:
                    logger.error(f"Failed to store encrypted simulation reply: {e}")
            
            return ChatResponse(
                reply=reply,
                intent="general_prompt",
                suggested_action=None
            )

        client = get_llm_client(request.provider if hasattr(request, 'provider') else None, use_fast=True)
        llm = client.chat_model

        # Define the Agent
        tools = [get_legal_context, get_platform_navigation]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a highly intelligent Indian Legal AI Advisor.
            Your goal is to assist users with legal queries using the 'get_legal_context' tool or guide them to platform features using 'get_platform_navigation'.
            
            Guidelines:
            1. If the user asks a specific legal question or needs knowledge, use 'get_legal_context'. 
            2. If the user wants to perform a task (draft, summary, etc.), use 'get_platform_navigation' to find the route.
            3. Always synthesize the information retrieved from tools into a helpful, conversational response.
            4. If you used legal context, ensure your response references the statutes or cases found.
            
            Response Requirement: You MUST return your final response as a JSON-compatible string that matches the structure:
            {{ "reply": "...", "intent": "one of [research, navigation, general]", "suggested_action": "/route or null", "citations": [{{ "title": "...", "source": "...", "text": "..." }}] or null }}
            """),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        response = await agent_executor.ainvoke({"input": user_message})
        output = response.get("output", "{}")

        try:
            import re
            json_match = re.search(r'(\{.*\})', output, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
            else:
                result = {"reply": output, "intent": "general", "suggested_action": None, "citations": None}
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse agent JSON: {e}. Output was: {output}")
            result = {"reply": output, "intent": "general", "suggested_action": None, "citations": None}

        # 2. Store assistant reply if user logged in (encrypted)
        final_reply = result.get("reply", "I can help with that.")
        if user_id:
            try:
                enc_assistant_msg = encryption_service.encrypt(final_reply)
                db_service.store_chat_message(user_id, encrypted_data=enc_assistant_msg)
            except Exception as e:
                logger.error(f"Failed to store encrypted assistant reply: {e}")

        # Map list of dicts to Citation objects if present
        citations = []
        if result.get("citations"):
            for c in result["citations"]:
                citations.append(Citation(title=c.get("title"), source=c.get("source"), text=c.get("text")))

        return ChatResponse(
            reply=final_reply,
            intent=result.get("intent", "general"),
            suggested_action=result.get("suggested_action"),
            citations=citations if citations else None
        )

    except Exception as e:
        logger.error(f"Error in chat_assistant agent: {e}")
        return ChatResponse(
            reply="I encountered an error processing your query. Please try again.",
            intent="error",
            suggested_action=None
        )

@router.get(
    "/history",
    summary="Get encrypted/plaintext chat history"
)
async def get_history(user_id: str = Query(..., description="User ID to fetch history for")):
    try:
        raw_messages = db_service.get_chat_history(user_id)
        formatted_messages = []
        
        for msg in raw_messages:
            content = msg.get("content") # Legacy plaintext
            is_encrypted = msg.get("is_encrypted", False)
            encrypted_content_b64 = msg.get("encrypted_content")
            
            if is_encrypted and encrypted_content_b64:
                try:
                    # Supabase returns bytes as Base64 strings or hex sometimes via Python client
                    # The library usually handles it, but let's be safe
                    if isinstance(encrypted_content_b64, str):
                        # Some Supabase implementations return '\x...' hex strings
                        if encrypted_content_b64.startswith('\\x'):
                            encrypted_bytes = bytes.fromhex(encrypted_content_b64[2:])
                        else:
                            encrypted_bytes = base64.b64decode(encrypted_content_b64)
                    else:
                        encrypted_bytes = encrypted_content_b64
                    
                    decrypted_content = encryption_service.decrypt(encrypted_bytes)
                    content = decrypted_content
                except Exception as e:
                    logger.error(f"Failed to decrypt message {msg.get('id')}: {e}")
                    content = "[Error: Decryption Failed]"
            
            formatted_messages.append({
                "id": str(msg.get("id")),
                "content": content,
                "role": "user" if msg.get("user_id") == user_id else "assistant", # Simplified role logic for history
                "created_at": msg.get("created_at"),
                "is_encrypted": is_encrypted
            })
            
        return formatted_messages
    except Exception as e:
        logger.error(f"Error fetching chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")
