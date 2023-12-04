from sqlalchemy.orm import Session, Query

from models import Item
from schermas import ItemCreate, ItemUpdate, ItemResponse

# 全建取得
def get_all(db: Session):
    return db.query(Item).all()

# id取得
def get_by_id(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

# name取得
def get_by_name(db: Session, item_name: str):
    return db.query(Item).filter(Item.name.like(f'%{item_name}%')).all()

# 新規作成
def crete(db: Session, post_item: ItemCreate, user_id: int):
    new_item = Item(
        **post_item.model_dump(),
        user_id=user_id
    )
    print(new_item)
    db.add(new_item)
    db.commit()
    return new_item

# 更新
def update(db: Session, item_id: int, post_item: ItemUpdate):
    item = get_by_id(db, item_id)
    if item is None:
        return None
    
    item.name = item.name if post_item.name is None else post_item.name
    item.price = item.price if post_item.price is None else post_item.price
    item.description = item.description if post_item.description is None else post_item.description
    item.status = item.status if post_item.status is None else post_item.status

    db.add(item)
    db.commit()
    return item

def delete(db, item_id):
    item = get_by_id(db, item_id)
    if item is None:
        return None
    
    db.delete(item)
    db.commit()
    return item