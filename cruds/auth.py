import hashlib
import base64
import os
from sqlalchemy.orm import Session
from schermas import UserCreate
from models import User


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
