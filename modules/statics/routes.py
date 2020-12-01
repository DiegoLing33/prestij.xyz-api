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

from fastapi import APIRouter, HTTPException
from pydantic.main import BaseModel

from blizzard.core import blizzard_db
from database import DatabaseUtils
from database.wowaccounts.models import WAccountModel
from modules.statics.models import StaticIndexModel, StaticMemberModel
from modules.statics.schemas import StaticIndex, StaticIndexCreate, StaticMemberCreate
from modules.statics.utils import StaticUtils
from wow.utils.users import BlizzardUsersUtils

router = APIRouter()


class AcceptCreate(BaseModel):
    token: str
    static_id: int
    member_id: int


@router.get(
    "/",
    summary='Возвращает список существующих статиков',
    response_model=List[StaticIndex]
)
def get_static_list():
    db = blizzard_db()
    return DatabaseUtils.core_query(db.query(StaticIndexModel)).all()


@router.post(
    "/",
    summary='Создает статик',
    response_model=StaticIndex
)
def create_static_(body: StaticIndexCreate):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    return StaticUtils.create_static(
        title=body.title,
        description=body.description,
        image=body.image,
        owner_blizzard_id=blizzard_id
    )


@router.post(
    '/members',
    summary="Создает анкету на участие в статике",
)
def add_player(body: StaticMemberCreate):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    db = blizzard_db()
    q = DatabaseUtils.core_query(db.query(WAccountModel)
                                 .filter(WAccountModel.user_id == blizzard_id)
                                 .filter(WAccountModel.wow_id == body.wow_id))
    if q.count() < 1:
        raise HTTPException(404, 'You have not got this player')
    return StaticUtils.add_player(
        static_id=body.static_id,
        wow_id=body.wow_id,
        role_id=body.role_id,
        comment=body.request_comment,
        blizzard_id=blizzard_id
    )


@router.post(
    '/members/accept',
    summary="Принемает заявку в статик",
)
def add_player(body: AcceptCreate):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    db = blizzard_db()
    qs = DatabaseUtils.core_query(db.query(StaticIndexModel)) \
        .filter(StaticIndexModel.owner_blizzard_id == blizzard_id)

    if qs.count() < 1:
        raise HTTPException(503, 'You cant accept player to not your static')

    q = DatabaseUtils.core_query(db.query(StaticMemberModel)) \
        .filter(StaticMemberModel.id == body.member_id)
    if q.count() < 1:
        raise HTTPException(404, 'You have not got this player')
    q.update({'request_state': 2})
    return True

# {
#   "title": "Первый статик гильдии 'Престиж'",
#   "description": "Первый статик гильдии World of Warcraft 'Престиж' на сервере Гордунни",
#   "image": "",
#   "token": "EUyYI130kEpCyHNgHihcC4Ze3MOjmds0L1"
# }


# {
#   "static_id": 1,
#   "role_id": 2,
#   "wow_id": 243679431,
#   "token": "EUyYI130kEpCyHNgHihcC4Ze3MOjmds0L1",
#   "request_comment": "РЛ"
# }
