from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import logging
from app.schemas import UsageRecordRequest, UsageHistoryResponse, UsageHistoryItem, ErrorResponse
from app.services.supabase_service import db_service
from app.services.encryption import encryption_service

router = APIRouter(
    prefix="/api/usage",
    tags=["Usage & History"]
)

logger = logging.getLogger(__name__)

@router.post(
    "/record",
    summary="Record encrypted usage output",
    responses={500: {"model": ErrorResponse}}
)
async def record_usage(request: UsageRecordRequest):
    """
    Records a document generation result. 
    Content is encrypted before storage.
    """
    try:
        user_id = request.user_id
        service_type = request.service_type
        prompt_title = request.prompt_title
        prompt_output = request.prompt_output
        
        logger.info(f"Recording usage for {user_id} ({service_type})")
        
        encrypted_data = None
        if prompt_output:
            try:
                encrypted_data = encryption_service.encrypt(prompt_output)
                logger.debug("Successfully encrypted prompt_output")
            except Exception as e:
                logger.error(f"Encryption failed for usage recording: {e}")
                raise HTTPException(status_code=500, detail=f"Encryption failed: {e}")

        logger.debug(f"Storing usage record in DB for user {user_id}")
        result = db_service.record_usage(
            user_id=user_id,
            service_type=service_type,
            prompt_title=prompt_title,
            encrypted_data=encrypted_data,
            prompt_output=None if encrypted_data else prompt_output
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to store usage record")
            
        return {"status": "success", "id": result[0].get("id") if result else None}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in record_usage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/history",
    response_model=UsageHistoryResponse,
    summary="Get user activity history (decrypted titles)"
)
async def get_history(user_id: str = Query(..., description="User ID to fetch history for")):
    """
    Fetches the last 50 activity items. 
    Note: Heavy output is NOT included in this list for performance.
    """
    try:
        raw_history = db_service.get_usage_history(user_id)
        
        formatted_history = []
        for item in raw_history:
            formatted_history.append(UsageHistoryItem(
                id=str(item.get("id")),
                user_id=str(item.get("user_id")),
                service_type=item.get("service_type"),
                created_at=item.get("created_at"),
                prompt_title=item.get("prompt_title"),
                is_encrypted=item.get("is_encrypted", False)
            ))
            
        return UsageHistoryResponse(history=formatted_history)
    except Exception as e:
        logger.error(f"Error in get_history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")

@router.get(
    "/history/{activity_id}",
    response_model=UsageHistoryItem,
    summary="Get full activity detail (decrypted output)"
)
async def get_activity_detail(activity_id: str):
    """
    Fetches the full detail of a specific activity, including decryption.
    """
    try:
        item = db_service.get_usage_detail(activity_id)
        if not item:
            raise HTTPException(status_code=404, detail="Activity not found")
            
        content = item.get("prompt_output")
        is_encrypted = item.get("is_encrypted", False)
        encrypted_output = item.get("encrypted_output")
        
        if is_encrypted and encrypted_output:
            try:
                # Same hex handling as chat.py
                if isinstance(encrypted_output, str):
                    if encrypted_output.startswith('\\x'):
                        encrypted_bytes = bytes.fromhex(encrypted_output[2:])
                    else:
                        import base64
                        encrypted_bytes = base64.b64decode(encrypted_output)
                else:
                    encrypted_bytes = encrypted_output
                    
                decrypted_content = encryption_service.decrypt(encrypted_bytes)
                content = decrypted_content
            except Exception as e:
                logger.error(f"Decryption failed for activity {activity_id}: {e}")
                content = "[Error: Decryption Failed]"
                
        return UsageHistoryItem(
            id=str(item.get("id")),
            user_id=str(item.get("user_id")),
            service_type=item.get("service_type"),
            created_at=item.get("created_at"),
            prompt_title=item.get("prompt_title"),
            prompt_output=content,
            is_encrypted=is_encrypted
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_activity_detail: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch activity detail")
