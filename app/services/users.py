from sqlalchemy.orm import Session
from app.models.Users import User
from app.dtos.CreateUserDto import CreateUserDto
from app.dtos.UserDto import UserDto

import uuid

# Caută un user după auth0_id
def get_user_by_id(db: Session, id: str):
    user = db.query(User).filter(User.id == id).first()
    if user:
        return UserDto.model_validate(user)
    return None
def get_user_by_auth0_id(db: Session, auth0_id: str):
    user = db.query(User).filter(User.auth0_id == auth0_id).first()
    if user:
        return UserDto.model_validate(user)
    return None

# Creează un user nou dacă nu există
def create_user(db: Session, user_data: CreateUserDto, auth0_id):
    db_user = User(
        id=uuid.uuid4(),
        auth0_id=auth0_id,
        name=user_data.name,
        email=user_data.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserDto.model_validate(db_user)

def update_user(db: Session, id: str, name: str = None, email: str = None):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        return None

    if name:
        user.name = name
    if email:
        user.email = email

    db.commit() # salvam in baza de date
    db.refresh(user) # actualizam obiectul din memorie cu ce e în baza de date
    return UserDto.model_validate(user)
