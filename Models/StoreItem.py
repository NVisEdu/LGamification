from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped as Type, mapped_column as props

from app_database import database as appdb


class StoreItemModel(appdb.modelBase):
    __tablename__ = 'store_items'

    id: Type[int] = props(Integer, primary_key=True)
    name: Type[str] = props(String(32))
    description: Type[str] = props(String(128))
    cost: Type[int]
    required_lvl: Type[int]
