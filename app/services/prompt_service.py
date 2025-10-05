from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.schema import Prompt
from app.models.prompt import PromptCreate, PromptRead, PromptUpdate

class PromptService:
    def __init__(self, session: Session):
        self.session = session

    def list_prompts(self, app_id: str = None) -> list[Prompt]:
        """List all prompts, optionally filtered by app_id."""
        query = self.session.query(Prompt)
        if app_id:
            query = query.filter(Prompt.app_id == app_id)
        return query.all()

    def get_prompt(self, prompt_id: int) -> Prompt | None:
        """Get a prompt by ID."""
        return self.session.query(Prompt).get(prompt_id)

    def get_active_prompt(self, app_id: str, prompt_key: str) -> Prompt | None:
        """Get the active version of a prompt by app_id and prompt_key."""
        return self.session.query(Prompt).filter(
            Prompt.app_id == app_id,
            Prompt.prompt_key == prompt_key,
            Prompt.is_active == True
        ).first()

    def create_prompt(self, prompt: PromptCreate) -> Prompt:
        """Create a new prompt with versioning support."""
        try:
            # latest_version = self.session.query(Prompt.version).filter(
            #     Prompt.app_id == prompt.app_id,
            #     Prompt.prompt_key == prompt.prompt_key
            # ).order_by(Prompt.version.desc()).limit(1).scalar_one_or_none() or 0

            latest_version = (
                self.session.query(Prompt.version)
                .filter(
                    Prompt.app_id == prompt.app_id, 
                    Prompt.prompt_key == prompt.prompt_key
                )
                .order_by(Prompt.version.desc())
                .limit(1)
                .first()
            )

            if latest_version:
                latest_version = latest_version.version
            else:
                latest_version = 0

            if prompt.is_active:
                self.session.query(Prompt).filter(
                    Prompt.app_id == prompt.app_id,
                    Prompt.prompt_key == prompt.prompt_key
                ).update({"is_active": False})

            new_prompt = Prompt(
                app_id=prompt.app_id,
                prompt_key=prompt.prompt_key,
                prompt_text=prompt.prompt_text,
                version=latest_version + 1,
                is_active=prompt.is_active,
                created_by=prompt.created_by
            )
            self.session.add(new_prompt)
            self.session.commit()
            return new_prompt
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Conflict creating prompt")

    def update_prompt(self, prompt_id: int, prompt: PromptUpdate) -> Prompt | None:
        """Update an existing prompt."""
        prompt_obj = self.get_prompt(prompt_id)
        if not prompt_obj:
            return None

        if prompt.prompt_text:
            prompt_obj.prompt_text = prompt.prompt_text

        if prompt.is_active is not None:
            if prompt.is_active:
                self.session.query(Prompt).filter(
                    Prompt.app_id == prompt_obj.app_id,
                    Prompt.prompt_key == prompt_obj.prompt_key,
                    Prompt.id != prompt_id
                ).update({"is_active": False})

            prompt_obj.is_active = prompt.is_active

        self.session.commit()
        self.session.refresh(prompt_obj)
        return prompt_obj

    def delete_prompt(self, prompt_id: int) -> bool:
        """Delete a prompt by ID."""
        prompt_obj = self.get_prompt(prompt_id)
        if not prompt_obj:
            return False
        self.session.delete(prompt_obj)
        self.session.commit()
        return True