#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
import time
from typing import List

from logzero import logger
from progress.bar import Bar

from blizzard.core import blizzard_db
from blizzard.guild import blizzard_guild_roster
from database import DatabaseUtils
from database.wow.models import CharacterModel, CharacterEquipmentModel
from wow.interface.blizzard_api import BlizzardAPI
from wow.interface.entity import CharacterCountableSlots


class CharacterUpdater:

    @staticmethod
    def update_character_info(name: str, role=0):
        data = BlizzardAPI.character(name)
        if data is None:
            return None
        db = blizzard_db()
        q = db.query(CharacterModel).filter(CharacterModel.wow_id == data.wow_id)
        if q.count() > 0:
            q.update({
                'name': data.name,
                'level': data.level,
                'gender': data.gender,
                'faction': data.faction,

                'role_index': role,

                'character_race_id': data.character_race_id,
                'character_class_id': data.character_class_id,
                'character_spec_id': data.character_spec_id,
            })
        else:
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
        return True

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
        res = CharacterUpdater.update_character_info(name, role)
        if res is not None:
            CharacterUpdater.update_equipment(name)

    @staticmethod
    def update_characters():
        data = blizzard_guild_roster()
        logger.info("Fixing missed...")
        CharacterUpdater.fix_missed(data['members'])
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

    @staticmethod
    def fix_missed(blizzard_characters: List):
        db = blizzard_db()
        q = DatabaseUtils.core_query(db.query(CharacterModel)).all()
        for character in q:
            found = False
            for b_ch in blizzard_characters:
                if b_ch['character']['name'] == character.name:
                    found = True
            if not found:
                logger.warn(character.name + " escape guild")
                db.query(CharacterModel).filter(CharacterModel.wow_id == character.wow_id).update({'state': 0})
                db.commit()
