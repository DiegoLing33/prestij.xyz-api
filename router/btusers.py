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

from fastapi import APIRouter

from blizzard.core import blizzard_db
from database import DatabaseUtils
from database.wow.schemas import WAccount
from database.wowaccounts.models import WAccountModel
from modules.waccount.utils import WAccountUtils
from wow.interface.entity import BlizzardUser, BlizzardUserCreate
from wow.utils.users import BlizzardUsersUtils

router = APIRouter()


@router.post(
    "/",
    response_model=BlizzardUser,
    summary="Creates the blizzard user"
)
def add_user(body: BlizzardUserCreate):
    """
    Adds the user
    :param body:
    :return:
    """
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    WAccountUtils.eval_token(body.token)
    return BlizzardUsersUtils.add(
        blizzard_id=blizzard_id,
        blizzard_name=body.blizzard_name
    )


@router.get(
    "/accounts/{blizzard_id}",
    response_model=List[WAccount],
    summary="Returns the blizzard accounts by id"
)
def get_full_user(blizzard_id: int, token: str):
    BlizzardUsersUtils.id__safe(token)
    WAccountUtils.eval_token(token)
    db = blizzard_db()
    return DatabaseUtils.core_query(db.query(WAccountModel).filter(WAccountModel.user_id == blizzard_id)).all()


@router.get(
    "/{blizzard_id}",
    response_model=BlizzardUser,
    summary="Returns the blizzard user by id"
)
def get_user(blizzard_id: int):
    """
    Returns blizzard user utils
    :param blizzard_id:
    :return:
    """
    return BlizzardUsersUtils.get(blizzard_id)
