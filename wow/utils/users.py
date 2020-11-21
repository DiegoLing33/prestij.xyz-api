#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from fastapi import HTTPException

from database import DatabaseUtils
from wow.blizzard.core import blizzard_oauth_validate, blizzard_db
from wow.database.models import BlizzardUserModel


class BlizzardUsersUtils:
    """
    Blizzard user utils
    """

    @staticmethod
    def validate(token: str):
        res = blizzard_oauth_validate(token)
        return res

    @staticmethod
    def id(token: str):
        """
        Returns the id or None
        :param token:
        :return:
        """
        res = BlizzardUsersUtils.validate(token)
        return int(res['user_name']) if 'user_name' in res else None

    @staticmethod
    def id__safe(token: str):
        """
        Returns the id or None
        :param token:
        :return:
        """
        blizzard_id = BlizzardUsersUtils.id(token)
        if blizzard_id is None:
            raise HTTPException(status_code=404, detail=f"User token is undefined")
        return blizzard_id

    @staticmethod
    def add(blizzard_id: int, blizzard_name: str):
        """
        Adds the blizzard user

        :param blizzard_id:
        :param blizzard_name:
        :return:
        """
        db = blizzard_db()
        q = db.query(BlizzardUserModel).filter(BlizzardUserModel.blizzard_id == blizzard_id)
        count = q.count()
        if count == 0:
            return DatabaseUtils.insert(
                db,
                BlizzardUserModel(
                    blizzard_id=blizzard_id,
                    blizzard_name=blizzard_name
                )
            )
        else:
            return q.first()

    @staticmethod
    def get(blizzard_id):
        """
        Returns the blizzard user by blizzard_id
        :param blizzard_id:
        :return:
        """
        db = blizzard_db()
        return DatabaseUtils.core_query(
            db.query(BlizzardUserModel).filter(BlizzardUserModel.blizzard_id == blizzard_id)
        ).first()
