# sqlalchemyのmodel
# DBのテーブルをpythonのクラスとして表現したもの
# modelによりDBのテーブルやカラムの構造を直感的に操作できる

from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime
from schermas import ItemStatus


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.ON_SALE)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())