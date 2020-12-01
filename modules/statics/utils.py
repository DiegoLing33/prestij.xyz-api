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

from blizzard.core import blizzard_db
from database import DatabaseUtils
from modules.statics.models import StaticIndexModel, StaticMemberModel


class StaticUtils:
    """
    Static utils
    """

    @staticmethod
    def create_static(title, description, image, owner_blizzard_id):
        """
        Creates the static
        :param owner_blizzard_id:
        :param title:
        :param description:
        :param image:
        :return:
        """
        db = blizzard_db()
        return DatabaseUtils.insert(db, StaticIndexModel(
            title=title,
            description=description,
            image=image,
            owner_blizzard_id=owner_blizzard_id
        ))

    @staticmethod
    def add_player(static_id, wow_id, role_id, comment, blizzard_id):
        db = blizzard_db()
        q = db.query(StaticMemberModel).filter(StaticMemberModel.static_id == static_id) \
            .filter(StaticMemberModel.wow_id == wow_id).filter(StaticMemberModel.blizzard_id == blizzard_id)
        if q.count() > 0:
            raise HTTPException(429, "You have already sent the request")
        return DatabaseUtils.insert(db, StaticMemberModel(
            static_id=static_id,
            wow_id=wow_id,
            role_id=role_id,
            request_state=1,
            request_comment=comment,
            blizzard_id=blizzard_id
        ))

    @staticmethod
    def prove_player(static_id, wow_id, blizzard_id):
        db = blizzard_db()
        q = db.qery(StaticMemberModel).filter(StaticMemberModel.static_id == static_id) \
            .filter(StaticMemberModel.wow_id == wow_id).filter(StaticMemberModel.blizzard_id == blizzard_id)
        if q.count() < 1:
            raise HTTPException(404, 'Request is undefined!')
        q.update({'request_state': 2})
        db.commit()
        return True
