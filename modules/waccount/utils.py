#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
import requests
from logzero import logger

from blizzard.core import blizzard_db
from database import DatabaseUtils
from database.wowaccounts.models import WAccountModel


class WAccountUtils:

    @staticmethod
    def get_data(token: str):
        r = requests.get(
            'https://eu.api.blizzard.com/profile/user/wow',
            params={
                'locale': 'ru_RU',
                'namespace': "profile-eu",
                'access_token': token
            }
        )
        __json = r.json()
        if 'wow_accounts' in __json and len(__json['wow_accounts']) > 0:
            return [__json['id'], __json['wow_accounts'][0]["characters"]]
        return [0, []]

    @staticmethod
    def eval_token(token: str):
        logger.info(f'Token: {token}, accounts:')
        blizzard_id, items = WAccountUtils.get_data(token)
        for account in items:
            WAccountUtils.add(
                blizzard_id=blizzard_id,
                wow_id=account['id'],
                name=account['name'],
                realm_id=account['realm']['id'],
                realm_title=account['realm']['name'],
                level=account['level'],
                faction=account['faction']['type']
            )

    @staticmethod
    def add(
            blizzard_id: int,
            wow_id: int,
            name: str,
            realm_id: int,
            realm_title: str,
            level: int,
            faction: str
    ):
        """
        Adds the character
        :param realm_title:
        :param blizzard_id:
        :param wow_id:
        :param name:
        :param realm_id:
        :param level:
        :param faction:
        :return:
        """
        db = blizzard_db()
        q = DatabaseUtils.core_query(db.query(WAccountModel)) \
            .filter(WAccountModel.user_id == blizzard_id) \
            .filter(WAccountModel.wow_id == wow_id)

        if q.count() > 0:
            logger.info(f'Updates: {name}')
            q.update({
                'name': name,
                'realm_id': realm_id,
                'realm_title': realm_title,
                'level': level,
                'faction': faction,
            })
        else:
            logger.info(f'Creates: {name}')
            db.add(WAccountModel(
                user_id=blizzard_id,
                wow_id=wow_id,
                name=name,
                realm_id=realm_id,
                realm_title=realm_title,
                level=level,
                faction=faction
            ))
        db.commit()
