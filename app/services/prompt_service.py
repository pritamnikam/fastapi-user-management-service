from sqlalchemy.orm import Session
from app.db.schema import Prompt

class PromptService:
    """Service class for prompt CRUD operations."""

    def __init__(self, session: Session):
        self._db = session

    def list_prompts(self) -> list[Prompt]:
        return self._db.query(Prompt).all()

    def get_prompt(self, prompt_id: int) -> Prompt | None:
        return self._db.query(Prompt).filter(Prompt.id == prompt_id).first()

    def create_prompt(self, name: str, content: str, description: str | None = None) -> Prompt:
        prompt = Prompt(name=name, content=content, description=description)
        self._db.add(prompt)
        self._db.commit()
        self._db.refresh(prompt)
        return prompt

    def update_prompt(self, prompt_id: int, name: str, content: str, description: str | None = None) -> Prompt | None:
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return None
        prompt.name = name
        prompt.content = content
        prompt.description = description
        self._db.commit()
        self._db.refresh(prompt)
        return prompt

    def delete_prompt(self, prompt_id: int) -> bool:
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return False
        self._db.delete(prompt)
        self._db.commit()
        return True