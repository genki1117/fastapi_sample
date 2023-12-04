from datetime import datetime, timedelta
import hashlib
import base64
import os
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer # リクエストのauthorizationヘッダーからBearerを取得する
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from schermas import UserCreate, DecodedToken
from models import User

# tokenを取得するエンドポイントを引数にし、インスタンス化する
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") 

def create_user(db: Session, user_create: UserCreate):
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac('sha256', user_create.password.encode(), salt, 1000).hex()

    new_user = User(
        username = user_create.username,
        password = hashed_password,
        salt = salt.decode()
    )
    db.add(new_user)
    db.commit()
    return new_user

# userの認証処理
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    
    # 入力されたパスワードをハッシュ化
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), user.salt.encode(), 1000).hex()
    
    # 入力されたパスワードとDBに保存されているパスワードの照合
    if user.password != hashed_password:
        return None
    
    # 入力されたパスワードが正しかった場合
    return user


"""
jsonを作成、検証のためjson-joseライブラリをインストール
pip install "python-jose[cryptography]"
ターミナルで openssl rand -hex 32 を入力し秘密鍵を生成
"""
ALGORITHM = 'HS256'
SECRET_KEY = '0531bbdd66d7ac2737f3759ef7f5974c3e0212030492d69a0bc7a45a920679af'


# tokenの作成
# jwtに含めたい情報を引数に渡す
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    # トークンの有効期限
    # 現在の日時から引数に渡された時間を加算
    expires = datetime.now() + expires_delta

    # jwtのpayload部部に任意の情報をセット
    payload = {"sub": username, "id": user_id, "exp": expires}

    # jwtを生成
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# tokenからuser情報を取得する関数を定義
# Annotated[str, Depends(oauth2_scheme)でtoken変数にtokenを代入
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        # ヘッダーから取得したtokenとSECRET_KEYと、アルゴリズムを引数に渡してjwtのpayload部分を取得する
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        
        # 取得したusernameとuser_idが不正なら
        if username is None or user_id is None:
            return None
        
        # schemesからDecodedTokenを取得し、オブジェクトにしてreturn
        return DecodedToken(username=username, user_id=user_id)
    except JWTError:
        raise JWTError