from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.config import OPENAI_API_KEY
from app.llms import get_llm_client

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import logging
import json

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat Assistant"]
)

logger = logging.getLogger(__name__)

@router.post(
    "/chat-assistant",
    response_model=ChatResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Advisory Chat Assistant"
)
async def chat_assistant(request: ChatRequest):
    try:
        user_message = request.message
        logger.info(f"Received chat message: {user_message}")

        if not OPENAI_API_KEY:
            return ChatResponse(
                reply="[Simulation] I am a legal assistant. I can help you draft contracts, check compliance, or research laws. (OpenAI Key missing)",
                intent="general_prompt",
                suggested_action=None
            )

        # Use unified client factory with optional provider
        try:
            client = get_llm_client(request.provider if hasattr(request, 'provider') else None)
            llm = client.chat_model
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        # 1. Intent Classification and Response Generation
        # We ask the LLM to classify intent and generate a reply in one go (or JSON)
        
        prompt = PromptTemplate.from_template(
            """You are a helpful Legal Contract AI Assistant. Your goal is to guide the user to the right tools or answer general questions.
            
            Available Tools:
            - "drafting": For creating new contracts or clauses.
            - "compliance": For reviewing contracts against laws/policies.
            - "research": For finding case law and statutes.
            - "general_query": For general questions or greetings.
            
            User Message: {message}
            
            Return a JSON object with:
            - "intent": One of [drafting, compliance, research, general_query]
            - "reply": A helpful response to the user, suggesting the appropriate tool if applicable.
            - "suggested_action": null, or one of ["/contract-drafting", "/compliance-check", "/legal-research"] corresponding to the intent.
            """
        )
        
        chain = prompt | llm | JsonOutputParser()
        
        result = await chain.ainvoke({"message": user_message})
        
        return ChatResponse(
            reply=result.get("reply", "I can help with that."),
            intent=result.get("intent", "general_query"),
            suggested_action=result.get("suggested_action")
        )

    except Exception as e:
        logger.error(f"Error in chat_assistant: {e}")
        # Fallback for parsing errors or API errors
        return ChatResponse(
            reply="I encountered an error processing your request. How else can I help?",
            intent="error",
            suggested_action=None
        )
