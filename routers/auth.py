from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from cruds import auth as auth_cruds
from schermas import UserCreate, UserResponse
from database import get_db

router = APIRouter(prefix='/auth', tags=['auth'])

DbDependency = Annotated[Session, Depends(get_db)]


@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(db: DbDependency, user_create: UserCreate):
    return auth_cruds.create_user(db, user_create)