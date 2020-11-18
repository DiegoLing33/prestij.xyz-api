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
from core.utils import write_json
from database import DatabaseUtils
from wow.database.models import MythicRaceModel
from wow.interface.entity import MythicRace


class MythicAPIList(BaseModel):
    items: List[MythicRace]
    count: int


class MythicAPIListResponse(BaseModel):
    response: MythicAPIList
    request: RequestLimit


class MythicAPI:

    @staticmethod
    def list(db: Session, limit: int = 100, offset: int = 0):
        return DatabaseUtils.limited_results(db, MythicRaceModel, limit=limit, offset=offset)

    @staticmethod
    def by_hash(db: Session, mythic_hash: str):
        return db.query(MythicRaceModel).filter(MythicRaceModel.mythic_hash == mythic_hash).first()
