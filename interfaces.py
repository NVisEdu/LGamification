from typing import Type

from interface import Interface
from sqlalchemy.orm import DeclarativeBase


# ToDo Интерфейсы сломались; возможно дело в библиотеке

# class IRepository(Interface):
#     _Model: "DeclarativeBase"
#
#
# class IFacade(Interface):
#     _Repo: Type["IRepository"]
#     entry: Type["DeclarativeBase"]
#
#     def commit_changes(self):
#         ...
