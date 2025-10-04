"""API routes for user CRUD operations.

- GET /users: List all users
- POST /users: Create a new user
- GET /users/{user_id}: Get user by ID
- PUT /users/{user_id}: Update user
- DELETE /users/{user_id}: Delete user
"""

from fastapi import APIRouter, Depends, HTTPException

from app.db.schema import SessionLocal
from app.models.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


def get_user_service() -> UserService:
    """Dependency provider for UserService."""
    return UserService(session=SessionLocal())


@router.get("/users", response_model=list[UserRead])
def get_users(service: UserService = Depends(get_user_service)):
    """List all users."""
    return service.list_users()


@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """Create a new user."""
    return service.create_user(user.name)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Get a user by ID."""
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, user: UserCreate, service: UserService = Depends(get_user_service)
):
    """Update a user's name."""
    updated = service.update_user(user_id, user.name)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/users/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Delete a user by ID."""
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True}