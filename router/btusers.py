#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black

from fastapi import APIRouter

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
    return BlizzardUsersUtils.add(
        blizzard_id=blizzard_id,
        blizzard_name=body.blizzard_name
    )


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
