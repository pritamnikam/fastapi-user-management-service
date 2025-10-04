from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.db.schema import Prompt

class PromptService:
    """Service class for prompt CRUD operations."""

    def __init__(self, session: Session):
        self._db = session

    def list_prompts(self, app_id: str = None) -> list[Prompt]:
        """List all prompts, optionally filtered by app_id."""
        query = select(Prompt)
        if app_id:
            query = query.where(Prompt.app_id == app_id)
        return list(self._db.execute(query).scalars().all())

    def get_prompt(self, prompt_id: int) -> Prompt | None:
        """Get a prompt by ID."""
        return self._db.execute(
            select(Prompt).where(Prompt.id == prompt_id)
        ).scalar_one_or_none()

    def get_active_prompt(self, app_id: str, prompt_key: str) -> Prompt | None:
        """Get the active version of a prompt by app_id and prompt_key."""
        return self._db.execute(
            select(Prompt).where(
                (Prompt.app_id == app_id) &
                (Prompt.prompt_key == prompt_key) &
                (Prompt.is_active == True)
            )
        ).scalar_one_or_none()

    def create_prompt(self, app_id: str, prompt_key: str, prompt_text: str, 
                     created_by: str, is_active: bool = True) -> Prompt:
        """Create a new prompt with versioning support."""
        # Get the latest version number for this prompt_key
        latest_version = self._db.execute(
            select(Prompt.version)
            .where(
                (Prompt.app_id == app_id) & 
                (Prompt.prompt_key == prompt_key)
            )
            .order_by(Prompt.version.desc())
            .limit(1)
        ).scalar_one_or_none() or 0
        
        # If this will be active, deactivate all other versions
        if is_active:
            self._db.execute(
                update(Prompt)
                .where(
                    (Prompt.app_id == app_id) & 
                    (Prompt.prompt_key == prompt_key)
                )
                .values(is_active=False)
            )
        
        # Create the new prompt version
        prompt = Prompt(
            app_id=app_id,
            prompt_key=prompt_key,
            prompt_text=prompt_text,
            version=latest_version + 1,
            is_active=is_active,
            created_by=created_by
        )
        self._db.add(prompt)
        self._db.commit()
        self._db.refresh(prompt)
        return prompt

    def update_prompt(self, prompt_id: int, prompt_text: str = None, 
                     is_active: bool = None) -> Prompt | None:
        """Update an existing prompt."""
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return None
            
        if prompt_text is not None:
            prompt.prompt_text = prompt_text
            
        if is_active is not None:
            # If setting to active, deactivate all other versions
            if is_active:
                self._db.execute(
                    update(Prompt)
                    .where(
                        (Prompt.app_id == prompt.app_id) & 
                        (Prompt.prompt_key == prompt.prompt_key) &
                        (Prompt.id != prompt_id)
                    )
                    .values(is_active=False)
                )
            prompt.is_active = is_active
            
        self._db.commit()
        self._db.refresh(prompt)
        return prompt

    def delete_prompt(self, prompt_id: int) -> bool:
        """Delete a prompt by ID."""
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return False
        self._db.delete(prompt)
        self._db.commit()
        return True