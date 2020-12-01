#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from database.core.models import CoreModel
from database.wow.models import CharacterModel


class StaticMemberModel(Base, CoreModel):
    __tablename__ = "static_members"
    static_id = Column(Integer, ForeignKey("static_index.id"))
    request_state = Column(Integer, default=1)
    request_comment = Column(String)
    role_id = Column(Integer)

    wow_id = Column(Integer, ForeignKey("characters.wow_id"))
    blizzard_id = Column(Integer)
    character = relationship(CharacterModel)

    static = relationship("StaticIndexModel", back_populates="members")


class StaticIndexModel(Base, CoreModel):
    __tablename__ = "static_index"

    title = Column(String)
    description = Column(String)
    image = Column(String)
    owner_blizzard_id = Column(Integer)

    members = relationship(StaticMemberModel, back_populates="static")
