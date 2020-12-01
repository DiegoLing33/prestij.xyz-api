#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from typing import List, Optional

from pydantic import BaseModel

from wow.interface.entity import Character


class StaticMemberBase(BaseModel):
    static_id: int
    role_id: int
    wow_id: int
    blizzard_id: int

    request_state: int
    request_comment: str


class StaticMemberCreate(BaseModel):
    static_id: int
    role_id: int
    wow_id: int
    token: str
    request_comment: str


class StaticMember(StaticMemberBase):
    id: int
    character: Character

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaticIndexCreate(BaseModel):
    title: str
    description: str
    image: str
    token: str


class StaticIndexBase(BaseModel):
    title: str
    description: str
    image: str
    owner_blizzard_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaticIndex(StaticIndexBase):
    members: List[StaticMember]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
