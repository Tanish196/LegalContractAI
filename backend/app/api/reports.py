"""General report generation endpoints."""

import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas import InsightTaskRequest, InsightTaskResponse, ErrorResponse
from app.services.insight_service import generate_structured_report

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


@router.post(
    "/generate",
    response_model=InsightTaskResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Generate a structured legal report",
    description="Proxy endpoint that applies prompt engineering and Gemini to general-purpose legal tasks."
)
async def generate_report(request: InsightTaskRequest):
    try:
        logger.info("Generating %s report via structured LLM prompt", request.task_type)
        markdown = await generate_structured_report(
            task_type=request.task_type,
            content=request.content,
            jurisdiction=request.jurisdiction,
            metadata=request.metadata,
        )
        return InsightTaskResponse(
            task_type=request.task_type,
            report_markdown=markdown,
            metadata={"jurisdiction": request.jurisdiction}
        )
    except Exception as exc:
        logger.error("Error generating report: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )
