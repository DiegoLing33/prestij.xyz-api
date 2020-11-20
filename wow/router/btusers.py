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

from database import get_db, DatabaseUtils
from wow.database.models import PostCategoryModel, BTUserModel
from wow.interface.entity import PostCategory, BTUser

router = APIRouter()


@router.post(
    "/",
    response_model=BTUser,
    summary="Adds the user"
)
def add_user(body: BTUser, db=Depends(get_db)):
    return DatabaseUtils.insert(db, BTUserModel(
        bt_id=body.bt_id,
        bt_title=body.bt_title,
        name=body.name,
    ))


@router.get(
    "/{bt_id}",
    response_model=BTUser,
    summary="Returns the user"
)
def get_user(bt_id: int, db=Depends(get_db)):
    return db.query(BTUserModel).filter(BTUserModel.bt_id == bt_id).first()

