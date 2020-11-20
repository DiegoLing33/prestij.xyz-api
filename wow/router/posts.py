#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from typing import List

from fastapi import APIRouter, Depends

from core.response import RequestLimit
from database import get_db, DatabaseUtils
from wow.database.models import PostCategoryModel, PostModel
from wow.interface.entity import PostCategory, Post
from wow.utils.posts import PostsUtils

from pydantic import BaseModel

router = APIRouter()


class PostAPIList(BaseModel):
    items: List[Post]
    count: int


class PostAPIListResponse(BaseModel):
    response: PostAPIList
    request: RequestLimit


@router.post(
    "/categories",
    response_model=PostCategory,
    summary='Adds the category'
)
def add_category(body: PostCategory):
    return PostsUtils.add_category(body.user_id, body.title, body.url)


@router.post(
    "/",
    response_model=Post,
    summary='Adds the post'
)
def add_post(body: Post, db=Depends(get_db)):
    return DatabaseUtils.insert(db, PostModel(
        user_id=body.user_id,
        category_id=body.category_id,

        title=body.title,
        content=body.content,
        tags=body.tags
    ))


@router.get(
    "/category/{category_id}",
    response_model=PostAPIListResponse,
    summary='Adds the post'
)
def get_posts(category_id: int, limit: int = 100, offset: int = 0, db=Depends(get_db)):
    return DatabaseUtils.limited_results_query(
        db.query(PostModel).filter(PostModel.category_id == category_id),
        limit=limit,
        offset=offset
    )


@router.get(
    "/",
    response_model=PostAPIListResponse,
    summary='Adds the post'
)
def get_posts_all(category_id: int, limit: int = 100, offset: int = 0, db=Depends(get_db)):
    return DatabaseUtils.limited_results(
        db,
        PostModel,
        limit=limit,
        offset=offset
    )


@router.get(
    "/{post_id}",
    response_model=Post,
    summary='Returns the post'
)
def get_post(post_id: int, db=Depends(get_db)):
    return db.query(PostModel).filter(PostModel.id == post_id).first()


@router.get(
    "/categories",
    response_model=List[PostCategory],
    summary='Returns the categories'
)
def get_categories(db=Depends(get_db)):
    return db.query(PostCategoryModel).all()
