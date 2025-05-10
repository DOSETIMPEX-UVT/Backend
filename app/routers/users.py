from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.users import create_user, get_user_by_id, update_user, get_user_by_auth0_id
from app.dtos.UserDto import UserDto
from app.dtos.CreateUserDto import CreateUserDto
from app.dtos.UpdateUserDto import UpdateUserDto

from app.auth import get_current_user  # funcția care validează tokenul și extrage userul

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Creare user nou
@router.post("/create_user", response_model=UserDto)
def create_new_user(
    create_user_data: CreateUserDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # validare token Auth0
):
    auth0_id = current_user["sub"]  # extragem auth0_id-ul din token
    existing_user = get_user_by_auth0_id(db, auth0_id)
    if existing_user:
        return existing_user
    return create_user(db, create_user_data, auth0_id)

@router.put("/update_user/{id}", response_model=UserDto)
def update_existing_user(
    id: str,
    user_data: UpdateUserDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # validare token Auth0
):
    updated_user = update_user(db, id, name=user_data.name, email=user_data.email)
    if updated_user:
        return updated_user
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Găsește user după auth0_id
@router.get("/profile/{id}", response_model=UserDto)
def get_user(
    id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # validare token Auth0
):
    user = get_user_by_id(db, id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/me", response_model=UserDto)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    auth0_id = current_user["sub"]
    user = get_user_by_auth0_id(db, auth0_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
