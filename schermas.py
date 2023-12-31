from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


# 商品のステータスをenumで定義
class ItemStatus(Enum):
    ON_SALE = 'ON_SALE'
    SOLD_OUT = 'SOLD_OUT'


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20, examples=['PC'])
    price: int = Field(gt=0, examples=[100000])
    description: Optional[str] = Field(default=None, examples=['美品です'])

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=20, examples=['PC'])
    price: Optional[int] = Field(default=None, gt=0, examples=[100000])
    description: Optional[str] = Field(default=None, examples=['美品です'])
    status: Optional[ItemStatus] = Field(default=None, examples=[ItemStatus.SOLD_OUT])

class ItemResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    name: str = Field(min_length=2, max_length=20, examples=['PC'])
    price: int = Field(gt=0, examples=[100000])
    description: Optional[str] = Field(default=None, examples=['美品です'])
    status: ItemStatus = Field(examples=[ItemStatus.ON_SALE])
    created_at: datetime
    updated_at: datetime

    # この記述によりORMのmodelオブジェクトを適切なレスポンススキーマに変換する
    model_config = ConfigDict(from_attributes=True)