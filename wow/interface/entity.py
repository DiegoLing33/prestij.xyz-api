#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

CharacterEquipmentTypesList = [
    "HEAD", "NECK", "SHOULDER", "CHEST", "SHIRT"

    # Пояс
                                         "WAIST",
    "LEGS",

    # Ступни
    "FEET",

    # Запястья
    "WRIST",

    # Кисти рук
    "HANDS",

    "FINGER_1",
    "FINGER_2",
    "TRINKET_1",
    "TRINKET_2",

    "BACK"
    "MAIN_HAND",
    "OFF_HAND",

    # Накидка
    "TABARD",
]

CharacterCountableSlots = [
    "HEAD", "NECK", "SHOULDER", "CHEST", "WAIST", "LEGS", "FEET",
    "WRIST", "HANDS", "FINGER_1", "FINGER_2", "TRINKET_1", "TRINKET_2",
    "BACK", "MAIN_HAND", "OFF_HAND"
]


class CharacterEquipment(BaseModel):
    """
    Entity of the equipment item

    For e.g. hand
    """
    wow_id: int
    character_id: int
    image_id: Optional[int]

    title: str

    slot: str
    inventory_type: str
    level: int

    quantity: int
    quality: str

    item_class_id: int
    item_subclass_id: int

    stats: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CharacterRace(BaseModel):
    wow_id: int
    title: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CharacterRole(BaseModel):
    role_index: int
    title: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CharacterClass(BaseModel):
    wow_id: int
    title: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CharacterActiveSpec(BaseModel):
    wow_id: int
    title: str
    type: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Character(BaseModel):
    wow_id: int

    name: str
    gender: str
    level: int
    gear: Optional[int]
    meta_text: Optional[str]
    guild_role: Optional[str]

    role_index: Optional[int]
    role: Optional[CharacterRole]

    faction: str

    character_race_id: int
    character_race: Optional[CharacterRace]

    character_class_id: int
    character_class: Optional[CharacterClass]

    character_spec_id: int
    character_spec: Optional[CharacterActiveSpec]

    realm_id: int
    guild_id: int

    activity: int

    equipment: Optional[List[CharacterEquipment]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MythicRaceMember(BaseModel):
    wow_id: int
    name: str

    from_guild: bool

    spec_id: int
    spec: Optional[CharacterActiveSpec]

    mythic_hash: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MythicRaceAffix(BaseModel):
    wow_id: int
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MythicRace(BaseModel):
    mythic_hash: str
    team_hash: str
    affixes_hash: str

    wow_dung_id: int
    name: str
    guild_race: int

    level: int

    completed: int
    duration: int
    duration_string: str

    done_in_time: bool

    members: Optional[List[MythicRaceMember]]
    affixes: Optional[List[MythicRaceAffix]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Post(BaseModel):
    pass


# ------------------------------------
#            BLIZZARD USER
# ------------------------------------

class BlizzardUserBase(BaseModel):
    blizzard_name: str


class BlizzardUserCreate(BlizzardUserBase):
    token: str


class BlizzardUser(BlizzardUserBase):
    id: int
    blizzard_id: int
    created: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# ------------------------------------
#            POST COMMENT
# ------------------------------------

class PostCommentBase(BaseModel):
    reply_id: Optional[int]
    post_id: int
    text: str


class PostCommentCreate(PostCommentBase):
    token: str


class PostComment(PostCommentBase):
    id: int

    user_id: int

    created: datetime

    post: Post
    user: BlizzardUser

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# ------------------------------------
#            POST CATEGORY
# ------------------------------------

class PostCategoryBase(BaseModel):
    title: str
    url: str


class PostCategoryCreate(PostCategoryBase):
    token: str


class PostCategory(PostCategoryBase):
    id: int

    user_id: int
    created: datetime

    user: BlizzardUser

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# ------------------------------------
#            POST LIKES
# ------------------------------------


class PostLikeBase(BaseModel):
    post_id: int


class PostLikeCreate(PostLikeBase):
    token: str


class PostLike(PostLikeBase):
    id: int

    user_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# ------------------------------------
#            POST
# ------------------------------------

class PostBase(BaseModel):
    title: str
    category_id: int
    content: str
    tags: str
    image: str


class PostCreate(PostBase):
    token: str


class Post(PostBase):
    id: Optional[int]

    user_id: int
    created: datetime

    category: PostCategory
    likes: List[PostLike]
    comments: List[PostComment]
    user: BlizzardUser

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
