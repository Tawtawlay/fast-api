from typing import Annotated

# Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext

# Local applications imports 
from database import SessionLocal
from models import Users


router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


class CreateUserRequest(BaseModel):
    email: str = Field(min_length=5, max_lengt=254)
    username: str = Field(min_length=3, max_length=30)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    password: str
    role: str


# GET request
@router.get('/auth', status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
    return db.query(Users).all()

# POST request
@router.post('/auth', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user = db.query(Users).filter(Users.username == create_user_request.username).first()

    if existing_user:
        raise HTTPException(status_code=409, detail='Username already exists')
    
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )
    db.add(create_user_model)
    db.commit()


@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed auth'
    return 'Successful Auth'