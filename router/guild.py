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

from fastapi import APIRouter, Depends

from database import get_db
from database.client import DataStore
from database.schemas import DataStore as DataStoreType
from database.wow.models import CharacterModel

router = APIRouter()


@router.get(
    "/",
    summary="Returns the guild info",
    response_model=List[DataStoreType]
)
def guild_get_info(db=Depends(get_db)):
    return list(filter(lambda x: x.field != 'token', DataStore.list(db)))


@router.get(
    "/object",
    summary="Returns the guild info",
)
def guild_get_info_object(db=Depends(get_db)):
    o = {}
    for it in DataStore.list(db):
        if it.field != 'token':
            o[it.field] = it.value
    return o


@router.get(
    "/activity",
    summary="Returns the guild activity info",
)
def guild_get_activity(db=Depends(get_db)):
    players = db.query(CharacterModel).all()
    mx_player = None
    mx_activity = 0
    a_players = []

    for player in players:
        if player.activity > mx_activity:
            mx_player = player
            mx_activity = player.activity

    for player in players:
        a_players.append({
            'name': player.name,
            'wow_id': player.wow_id,
            'activity_points': player.activity,
            'activity': round(player.activity / mx_activity * 100) / 100,
        })

    return {
        'max_activity': mx_activity,
        'max_player': {
            'name': mx_player.name,
            'wow_id': mx_player.wow_id,
            'activity_points': mx_activity,
            'activity': 1
        },
        'players': a_players
    }


@router.get(
    "/{param}",
    summary="Returns the guild variable info",
    response_model=DataStoreType
)
def guild_get_info(param: str, db=Depends(get_db)):
    return DataStore.get(db, field=param)
