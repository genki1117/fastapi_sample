from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from cruds import auth as auth_cruds
from schermas import UserCreate, UserResponse, token
from database import get_db

router = APIRouter(prefix='/auth', tags=['auth'])

DbDependency = Annotated[Session, Depends(get_db)]

# OAuth2PasswordRequestFormをDIで使用する
FormDependency = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]

@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(db: DbDependency, user_create: UserCreate):
    return auth_cruds.create_user(db, user_create)

# login処理
"""
requestにパスワードが入力されているのでOAuth2PasswordRequestFormを使用
OAuth2PasswordRequestFormを使用するにはpython-multipartをインストール
pip install python-multipart
"""
@router.post('/login', status_code=status.HTTP_200_OK, response_model=token)
async def login(db: DbDependency, form_data: FormDependency):
    user = auth_cruds.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    
    # user認証が正しい場合
    # create_access_token関数を呼び出しtokenを生成し、返却する
    token = auth_cruds.create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}