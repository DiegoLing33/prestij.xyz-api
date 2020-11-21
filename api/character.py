#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.response import RequestLimit
from database import DatabaseUtils
from database.wow.models import CharacterModel
from wow.interface.entity import Character


class CharacterAPIList(BaseModel):
    items: List[Character]
    count: int


class CharacterAPIListResponse(BaseModel):
    response: CharacterAPIList
    request: RequestLimit


class CharacterAPI:

    @staticmethod
    def list(db: Session, limit: int = 100, offset: int = 0):
        return DatabaseUtils.limited_results(db, CharacterModel, limit=limit, offset=offset)

    @staticmethod
    def missed(db: Session, limit: int = 100, offset: int = 0):
        return DatabaseUtils.limited_results_query(db.query(CharacterModel).filter(CharacterModel.state == 0),
                                                   limit=limit, offset=offset, show_removed=True)
