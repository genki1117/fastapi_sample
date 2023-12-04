# sqlalchemyのmodel
# DBのテーブルをpythonのクラスとして表現したもの
# modelによりDBのテーブルやカラムの構造を直感的に操作できる

from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from schermas import ItemStatus


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.ON_SALE)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    # ForeignKeyの引数にはテーブル名.idを指定する
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # pythonのmodel間で関連付け 多なのでitems
    users = relationship('User', back_populates='items')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
    # pythonのmodel間で関連付け 1なので単数系
    items = relationship('Item', back_populates='user')
