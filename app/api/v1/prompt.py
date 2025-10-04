from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from app.db.schema import SessionLocal
from app.models.prompt import PromptCreate, PromptRead, PromptUpdate
from app.services.prompt_service import PromptService
from typing import Optional

router = APIRouter()

def get_prompt_service() -> PromptService:
    return PromptService(session=SessionLocal())

@router.get("/prompts", response_model=list[PromptRead])
def get_prompts(
    app_id: Optional[str] = Query(None, description="Filter prompts by application ID"),
    service: PromptService = Depends(get_prompt_service)
):
    return service.list_prompts(app_id=app_id)

@router.post("/prompts", response_model=PromptRead)
def create_prompt(prompt: PromptCreate, service: PromptService = Depends(get_prompt_service)):
    try:
        return service.create_prompt(
            app_id=prompt.app_id,
            prompt_key=prompt.prompt_key,
            prompt_text=prompt.prompt_text,
            created_by=prompt.created_by,
            is_active=prompt.is_active
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=f"Conflict creating prompt with key '{prompt.prompt_key}' for app '{prompt.app_id}'"
        )

@router.get("/prompts/{prompt_id}", response_model=PromptRead)
def get_prompt(prompt_id: int, service: PromptService = Depends(get_prompt_service)):
    prompt = service.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.get("/prompts/active/{app_id}/{prompt_key}", response_model=PromptRead)
def get_active_prompt(app_id: str, prompt_key: str, service: PromptService = Depends(get_prompt_service)):
    prompt = service.get_active_prompt(app_id, prompt_key)
    if not prompt:
        raise HTTPException(status_code=404, detail=f"No active prompt found for key '{prompt_key}' in app '{app_id}'")
    return prompt

@router.put("/prompts/{prompt_id}", response_model=PromptRead)
def update_prompt(prompt_id: int, prompt: PromptUpdate, service: PromptService = Depends(get_prompt_service)):
    updated = service.update_prompt(
        prompt_id=prompt_id,
        prompt_text=prompt.prompt_text,
        is_active=prompt.is_active
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return updated

@router.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: int, service: PromptService = Depends(get_prompt_service)):
    success = service.delete_prompt(prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"success": True}