"""Business logic for user operations."""

from sqlalchemy.orm import Session

from app.db.schema import User


class UserService:
    """Service class for user CRUD operations."""

    def __init__(self, session: Session):
        """Initializes with a database session."""
        self._db = session

    def list_users(self) -> list[User]:
        """Returns all users."""
        return self._db.query(User).all()

    def get_user(self, user_id: int) -> User | None:
        """Gets a user by ID."""
        return self._db.query(User).filter(User.id == user_id).first()

    def create_user(self, name: str) -> User:
        """Creates a new user."""
        user = User(name=name)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user_id: int, name: str) -> User | None:
        """Updates a user's name."""
        user = self.get_user(user_id)
        if not user:
            return None
        user.name = name
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """Deletes a user by ID."""
        user = self.get_user(user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True