#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black


from fastapi import APIRouter, Depends

from database import get_db
from wow.api.mythic import MythicAPIListResponse, MythicAPI
from wow.interface.entity import MythicRace

router = APIRouter()


@router.get(
    "/list",
    response_model=MythicAPIListResponse,
    summary="Returns all mythic races in the guild"
)
def get_mythic_list(offset: int = 0, limit: int = 100, db=Depends(get_db)):
    return MythicAPI.list(db, limit, offset)


@router.get(
    "/{mythic_hash}",
    response_model=MythicRace,
    summary="Returns mythic races by mythic hash"
)
def get_mythic_list(mythic_hash: str, db=Depends(get_db)):
    return MythicAPI.by_hash(db, mythic_hash)
