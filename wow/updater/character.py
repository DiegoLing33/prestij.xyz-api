#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
import sys
import time

from progress.bar import Bar
from logzero import logger

from wow.blizzard import blizzard_guild_roster
from wow.blizzard.core import blizzard_db
from wow.database.models import CharacterModel, CharacterEquipmentModel, MythicRaceMembersModel, MythicRaceModel, \
    MythicRaceAffixesModel
from wow.interface.blizzard_api import BlizzardAPI
from wow.interface.entity import CharacterCountableSlots
from wow.utils.mythic_utils import MythicUtils


class CharacterUpdater:

    @staticmethod
    def update_character_info(name: str, role=0):
        data = BlizzardAPI.character(name)
        db = blizzard_db()
        db.query(CharacterModel).filter(CharacterModel.wow_id == data.wow_id).delete()

        db.add(CharacterModel(
            wow_id=data.wow_id,

            name=data.name,
            level=data.level,
            gender=data.gender,
            faction=data.faction,

            role_index=role,

            character_race_id=data.character_race_id,
            character_class_id=data.character_class_id,
            character_spec_id=data.character_spec_id,

            realm_id=data.realm_id,
            guild_id=data.guild_id,
        ))
        db.commit()

    @staticmethod
    def update_equipment(name: str):
        data = BlizzardAPI.character_equipment(name)
        db = blizzard_db()

        # print("")
        # logger.info("Starting update character equipment " + name)
        # logger.info(f"Total count: {len(data)}")
        bar = Bar('Equipment ' + name, max=len(data), fill='█')

        db.query(CharacterEquipmentModel) \
            .filter(CharacterEquipmentModel.character_id == data[0].character_id).delete()

        k = 0
        ks = 0
        for item in data:
            if item.slot in CharacterCountableSlots:
                k += item.level
                ks = ks + 1

            db.add(CharacterEquipmentModel(
                title=item.title,
                wow_id=item.wow_id,
                character_id=item.character_id,

                slot=item.slot,
                inventory_type=item.inventory_type,
                level=item.level,

                quantity=item.quantity,
                quality=item.quality,

                item_class_id=item.item_class_id,
                item_subclass_id=item.item_subclass_id,
                stats=item.stats,
            ))
            bar.next()
            time.sleep(1 / 1000)
        gear = round(k / ks)
        db.query(CharacterModel).filter(CharacterModel.name == name).update({'gear': gear})
        db.commit()

    @staticmethod
    def update_character(name: str, role=0):
        CharacterUpdater.update_character_info(name, role)
        CharacterUpdater.update_equipment(name)

    @staticmethod
    def update_characters():
        data = blizzard_guild_roster()
        logger.info("Starting update characters...")
        logger.info(f"Total count: {len(data['members'])}")
        bar = Bar('Characters updating', max=len(data['members']), fill='█')
        for member in data['members']:
            name = member["character"]["name"]
            role = member["rank"]
            bar.bar_prefix = f" [{name}]: "
            CharacterUpdater.update_character(name, role)
            bar.next()
        print("")

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
        data = blizzard_db().query(CharacterModel).all()
        logger.info("Starting update characters mythic...")
        logger.info(f"Total count: {len(data)}")
        bar = Bar('Characters mythic updating', max=len(data), fill='█')
        for member in data:
            name = member.name
            CharacterUpdater.update_mythic_character(name)
            bar.next()
        print("")

    @staticmethod
    def update_guild_role(name: str, role: int):
        """
        Updates player guild role

        :param name:
        :param role:
        :return:
        """
        db = blizzard_db()
        db.query(CharacterModel).filter(CharacterModel.name == name).update({'guild_role': role})
        db.commit()

    @staticmethod
    def update_meta(name: str, meta: str):
        """
        Updates player meta

        :param name:
        :param meta:
        :return:
        """
        db = blizzard_db()
        db.query(CharacterModel).filter(CharacterModel.name == name).update({'meta_text': meta})
        db.commit()
