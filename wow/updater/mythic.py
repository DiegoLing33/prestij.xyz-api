#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from logzero import logger
from progress.bar import Bar

from blizzard.core import blizzard_db
from database import DatabaseUtils
from database.wow.models import MythicRaceMembersModel, CharacterModel, MythicRaceModel, MythicRaceAffixesModel
from wow.utils.mythic_utils import MythicUtils


class MythicUpdater:

    @staticmethod
    def update_mythic_character(name):
        data = MythicUtils.get_profile_mythic(name)
        db = blizzard_db()
        print("")
        logger.info("Starting update character mythic " + name)
        bar = Bar('Mythic updating', max=len(data), fill='█')
        for item in data:
            g_race = 0
            for member in item['members']:
                ex_m = db.query(MythicRaceMembersModel) \
                    .filter(MythicRaceMembersModel.mythic_hash == item['hashes']['mythic']) \
                    .filter(MythicRaceMembersModel.wow_id == member['wow_id']).count()

                from_g = db.query(CharacterModel).filter(CharacterModel.wow_id == member['wow_id']).count() > 0
                if from_g:
                    g_race = g_race + 1

                if ex_m == 0:
                    db.add(MythicRaceMembersModel(
                        mythic_hash=item['hashes']['mythic'],
                        wow_id=member['wow_id'],
                        name=member['name'],
                        spec_id=member['spec']['wow_id'],
                        from_guild=from_g
                    ))
                    db.commit()

            ex = db.query(MythicRaceModel).filter(MythicRaceModel.mythic_hash == item['hashes']['mythic']).count()
            if ex == 0:
                db.add(MythicRaceModel(
                    team_hash=item['hashes']['team'],
                    affixes_hash=item['hashes']['affixes'],
                    mythic_hash=item['hashes']['mythic'],
                    wow_dung_id=item['wow_dung_id'],
                    name=item['name'],
                    completed=item['completed'],
                    duration=item['duration']['time'],
                    duration_string=item['duration']['format'],
                    done_in_time=item['done_in_time'],
                    guild_race=g_race,
                    level=item['keystone_level']
                ))
                db.commit()

            # Adding an affixes
            for affix in item['keystone_affixes']:
                ex_a = db.query(MythicRaceAffixesModel) \
                    .filter(MythicRaceAffixesModel.mythic_hash == item['hashes']['mythic']) \
                    .filter(MythicRaceAffixesModel.wow_id == affix['wow_id']).count()
                if ex_a == 0:
                    db.add(MythicRaceAffixesModel(
                        mythic_hash=item['hashes']['mythic'],
                        wow_id=affix['wow_id'],
                        name=affix['name'],
                    ))
                    db.commit()
            bar.next()
        print("")

    @staticmethod
    def update_characters_mythic():
        data = DatabaseUtils.core_query(blizzard_db().query(CharacterModel)).all()
        logger.info("Starting update characters mythic...")
        logger.info(f"Total count: {len(data)}")
        bar = Bar('Characters mythic updating', max=len(data), fill='█')
        for member in data:
            name = member.name
            MythicUpdater.update_mythic_character(name)
            bar.next()
        print("")
