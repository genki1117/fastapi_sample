from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from cruds import item as item_cruds, auth as auth_cruds
from schermas import ItemCreate, ItemUpdate, ItemResponse, DecodedToken

router = APIRouter(prefix='/items', tags=['items'])

DbDependency = Annotated[Session, Depends(get_db)]

# get_current_userからDecodedToken型でtokenを取得
# UserDependencyを設定する事で認証が必要になる
UserDependency = Annotated[DecodedToken, Depends(auth_cruds.get_current_user)]

# 全建取得
@router.get('', response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def get_all(db: DbDependency):
    return item_cruds.get_all(db)

# id取得
#  認証
@router.get('/{item_id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def get_by_id(db: DbDependency, user: UserDependency, item_id: int = Path(gt=0)):
    find_by_id = item_cruds.get_by_id(db, item_id, user.user_id)
    if not find_by_id:
        raise HTTPException(status_code=404, detail='item not found')
    return find_by_id

# name取得
@router.get('/', response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_by_name(db: DbDependency, item_name: str = Query(min_length=2, max_length=20)):
    find_by_name = item_cruds.get_by_name(db, item_name)
    if not find_by_name:
        raise HTTPException(status_code=404, detail='item not found')
    return find_by_name

# 新規作成
@router.post('/create', response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
# user: UserDependencyでauthorizationヘッダーからtokenを取得し、decodeしたDecodedToken型のオブジェクトを格納　
async def create(db: DbDependency, user: UserDependency, post_item: ItemCreate):
    return item_cruds.crete(db, post_item, user.user_id)

# 更新
@router.put('/update/{item_id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update(db: DbDependency,user: UserDependency,  post_item: ItemUpdate, item_id: int = Path(gt=0)):
    updated_item = item_cruds.update(db, item_id, post_item, user.user_id)
    if not updated_item:
        raise HTTPException(status_code=404, detail='item not updated')
    return updated_item

# 削除
@router.delete('/delete/{item_id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def delete(db: DbDependency, user: UserDependency,item_id:int = Path(gt=0)):
    deleted_item = item_cruds.delete(db, item_id, user.user_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail='item not deleted')
    return deleted_item