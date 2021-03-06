#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from database import Base
from database.core.models import CoreModel


class CharacterRaceModel(Base, CoreModel):
    __tablename__ = "characters_races"
    wow_id = Column(Integer)
    title = Column(String)


class CharacterRoleModel(Base, CoreModel):
    __tablename__ = "characters_roles"
    role_index = Column(Integer)
    title = Column(String)


class CharacterClassModel(Base, CoreModel):
    __tablename__ = "characters_classes"
    wow_id = Column(Integer)
    title = Column(String)


class CharacterSpecModel(Base, CoreModel):
    __tablename__ = "characters_specs"
    wow_id = Column(Integer)
    type = Column(Integer)
    title = Column(String)


class CharacterEquipmentModel(Base, CoreModel):
    __tablename__ = "characters_equipment"

    wow_id = Column(Integer)
    character_id = Column(Integer, ForeignKey("characters.wow_id"))

    title = Column(String)
    image_id = Column(Integer)

    slot = Column(String)
    inventory_type = Column(String)
    level = Column(Integer)

    quantity = Column(Integer)
    quality = Column(String)

    item_class_id = Column(Integer)
    item_subclass_id = Column(Integer)

    stats = Column(String)

    character = relationship("CharacterModel", back_populates="equipment")


class CharacterModel(Base, CoreModel):
    """
    User meta model
    """
    __tablename__ = "characters"

    wow_id = Column(Integer)

    name = Column(String)
    level = Column(Integer)
    gender = Column(String)
    faction = Column(String)
    gear = Column(Integer, default=0)

    guild_role = Column(Integer, default=0)
    meta_text = Column(String, default='')

    role_index = Column(Integer, ForeignKey("characters_roles.role_index"))
    role = relationship("CharacterRoleModel")

    character_race_id = Column(Integer, ForeignKey("characters_races.wow_id"))
    character_race = relationship("CharacterRaceModel")

    character_class_id = Column(Integer, ForeignKey("characters_classes.wow_id"))
    character_class = relationship("CharacterClassModel")

    character_spec_id = Column(Integer, ForeignKey("characters_specs.wow_id"))
    character_spec = relationship("CharacterSpecModel")

    activity = Column(Integer, default=0)

    realm_id = Column(Integer)
    guild_id = Column(Integer)

    equipment = relationship("CharacterEquipmentModel", back_populates="character")


class MythicRaceAffixesModel(Base, CoreModel):
    __tablename__ = "mythic_races_affixes"

    mythic_hash = Column(String, ForeignKey("mythic_races.mythic_hash"))
    wow_id = Column(Integer)
    name = Column(String)

    mythic = relationship("MythicRaceModel", back_populates="affixes")


class MythicRaceMembersModel(Base, CoreModel):
    __tablename__ = 'mythic_races_members'

    mythic_hash = Column(String, ForeignKey("mythic_races.mythic_hash"))

    wow_id = Column(Integer)
    name = Column(String)

    from_guild = Column(Boolean)

    spec_id = Column(Integer, ForeignKey('characters_specs.wow_id'))
    spec = relationship('CharacterSpecModel')

    mythic = relationship("MythicRaceModel", back_populates="members")


class MythicRaceModel(Base, CoreModel):
    __tablename__ = "mythic_races"

    team_hash = Column(String)
    affixes_hash = Column(String)
    mythic_hash = Column(String)

    level = Column(Integer)

    wow_dung_id = Column(Integer)
    name = Column(String)
    guild_race = Column(Integer)

    completed = Column(Integer)
    duration = Column(Integer)
    duration_string = Column(String)

    done_in_time = Column(Boolean)

    members = relationship("MythicRaceMembersModel", back_populates="mythic")
    affixes = relationship("MythicRaceAffixesModel", back_populates="mythic")


class BlizzardUserModel(Base, CoreModel):
    __tablename__ = "blizzard_users"

    blizzard_id = Column(Integer)
    blizzard_name = Column(String)


class PostCommentsModel(Base, CoreModel):
    __tablename__ = "posts_comments"

    user_id = Column(Integer, ForeignKey("blizzard_users.blizzard_id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    reply_id = Column(Integer)
    text = Column(String)

    post = relationship("PostModel", back_populates="comments")
    user = relationship("BlizzardUserModel")


class PostCategoryModel(Base, CoreModel):
    __tablename__ = "posts_categories"

    user_id = Column(Integer, ForeignKey("blizzard_users.blizzard_id"))
    title = Column(String)
    url = Column(String, default='')

    user = relationship("BlizzardUserModel")


class PostLikeModel(Base, CoreModel):
    __tablename__ = "posts_likes"

    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("blizzard_users.blizzard_id"))

    user = relationship("BlizzardUserModel")
    post = relationship("PostModel", back_populates="likes")


class PostModel(Base, CoreModel):
    __tablename__ = "posts"

    title = Column(String)
    user_id = Column(Integer, ForeignKey("blizzard_users.blizzard_id"))
    category_id = Column(Integer, ForeignKey("posts_categories.id"))
    image = Column(String)

    content = Column(String)
    tags = Column(String, default='')

    category = relationship("PostCategoryModel")
    likes = relationship("PostLikeModel", back_populates="post")
    comments = relationship("PostCommentsModel", back_populates="post")
    user = relationship("BlizzardUserModel")
