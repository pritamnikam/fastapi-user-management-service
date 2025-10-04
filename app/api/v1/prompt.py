from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.db.schema import SessionLocal
from app.models.prompt import PromptCreate, PromptRead
from app.services.prompt_service import PromptService

router = APIRouter()

def get_prompt_service() -> PromptService:
    return PromptService(session=SessionLocal())

@router.get("/prompts", response_model=list[PromptRead])
def get_prompts(service: PromptService = Depends(get_prompt_service)):
    return service.list_prompts()

@router.post("/prompts", response_model=PromptRead)
def create_prompt(prompt: PromptCreate, service: PromptService = Depends(get_prompt_service)):
    try:
        return service.create_prompt(prompt.name, prompt.content, prompt.description)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=f"Prompt with name '{prompt.name}' already exists."
        )

@router.get("/prompts/{prompt_id}", response_model=PromptRead)
def get_prompt(prompt_id: int, service: PromptService = Depends(get_prompt_service)):
    prompt = service.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.put("/prompts/{prompt_id}", response_model=PromptRead)
def update_prompt(prompt_id: int, prompt: PromptCreate, service: PromptService = Depends(get_prompt_service)):
    updated = service.update_prompt(prompt_id, prompt.name, prompt.content, prompt.description)
    if not updated:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return updated

@router.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: int, service: PromptService = Depends(get_prompt_service)):
    success = service.delete_prompt(prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"success": True}