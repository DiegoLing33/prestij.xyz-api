#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black

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

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.response import RequestLimit
from database import get_db, DatabaseUtils
from database.wow.models import PostModel, PostCommentsModel
from wow.interface.entity import PostCategory, Post, PostCategoryCreate, PostCreate, PostLikeCreate, PostCommentCreate
from wow.utils.posts import PostsUtils
from wow.utils.users import BlizzardUsersUtils

router = APIRouter()


class TokenArgs(BaseModel):
    token: str


class TokenPostIdArgs(BaseModel):
    token: str
    post_id: int


class CommentIdAndToken(TokenArgs):
    comment_id: int


class PostAPIList(BaseModel):
    items: List[Post]
    count: int


class PostAPIListResponse(BaseModel):
    response: PostAPIList
    request: RequestLimit


# -----------------------------------
#            CATEGORIES
# -----------------------------------

@router.post(
    "/categories",
    response_model=PostCategory,
    summary='Adds the category'
)
def add_category(body: PostCategoryCreate):
    """
    Adds the category

    :param body:
    :return:
    """
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    return PostsUtils.add_category(user_id=blizzard_id, url=body.url, title=body.title)


@router.get(
    "/categories",
    response_model=List[PostCategory],
    summary='Returns the categories'
)
def get_categories():
    """
    Returns the categories list
    :return:
    """
    return PostsUtils.get_categories()


# -----------------------------------
#              POSTS
# -----------------------------------

@router.get(
    "/",
    response_model=PostAPIListResponse,
    summary='Returns all the posts'
)
def get_posts_all(limit: int = 100, offset: int = 0):
    return PostsUtils.get_posts_limit(
        limit=limit,
        offset=offset
    )


@router.get(
    "/category/{category_url}",
    response_model=PostAPIListResponse,
    summary='Returns the posts in category'
)
def get_posts_all(category_url: int, limit: int = 100, offset: int = 0):
    """
    Returns all the posts by category
    :param category_url:
    :param limit:
    :param offset:
    :return:
    """
    return PostsUtils.get_posts_by_category_limit(
        category_id=category_url,
        limit=limit,
        offset=offset
    )


@router.get(
    "/user/{blizzard_id}",
    response_model=PostAPIListResponse,
    summary='Returns the posts by users'
)
def get_posts_all(blizzard_id: int, limit: int = 100, offset: int = 0):
    """
    Returns all the posts by category
    :param blizzard_id:
    :param limit:
    :param offset:
    :return:
    """
    return PostsUtils.get_posts_by_blizzard_id(
        blizzard_id=blizzard_id,
        limit=limit,
        offset=offset
    )


@router.post(
    "/like",
    summary='Likes the post',
    tags=['Лайки']
)
def like_post(body: PostLikeCreate):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    return PostsUtils.add_like(
        user_id=blizzard_id,
        post_id=body.post_id,
    )


@router.post(
    "/unlike",
    summary='Unlikes the post',
    tags=['Лайки']
)
def like_post(body: PostLikeCreate):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    return PostsUtils.remove_like(
        user_id=blizzard_id,
        post_id=body.post_id,
    )


@router.post(
    "/comment",
    summary='Adds the comment',
    tags=['Комментарии']
)
def like_post(body: PostCommentCreate):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    return PostsUtils.add_comment(
        user_id=blizzard_id,
        post_id=body.post_id,
        reply_id=body.reply_id,
        text=body.text,
    )


@router.delete(
    "/comment",
    summary='Removes the comment',
    tags=['Комментарии']
)
def removes_post(body: CommentIdAndToken, db=Depends(get_db)):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    com = db.query(PostCommentsModel).filter(PostCommentsModel.id == body.comment_id).filter(
        PostCommentsModel.user_id == blizzard_id)
    if com.count() > 0:
        com.delete()
        db.commit()
        return True
    return False


@router.post(
    "/",
    response_model=Post,
    summary='Adds the post'
)
def add_post(body: PostCreate):
    """
    Adds the post item

    :param body:
    :return:
    """
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    return PostsUtils.add_post(
        user_id=blizzard_id,
        category_id=body.category_id,

        title=body.title,
        content=body.content,
        tags=body.tags,
        image=body.image
    )


@router.delete(
    "/{post_id}",
    summary='Deletes the post'
)
def delete_post(post_id: int, body: TokenArgs, db=Depends(get_db)):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    q = db.query(PostModel).filter(PostModel.id == post_id).filter(PostModel.user_id == blizzard_id)
    if q.count() == 0:
        raise HTTPException(status_code=404, detail='Post is undefined')
    return DatabaseUtils.remove_query(db, q)


@router.post(
    "/{post_id}",
    summary='Edits the post'
)
def edit_post(post_id: int, body: PostCreate, db=Depends(get_db)):
    blizzard_id = BlizzardUsersUtils.id__safe(body.token)
    q = db.query(PostModel).filter(PostModel.id == post_id).filter(PostModel.user_id == blizzard_id)
    if q.count() == 0:
        raise HTTPException(status_code=404, detail='Post is undefined')
    q.update({
        'title': body.title,
        'content': body.content,
        'category_id': body.category_id,
        'image': body.image,
        'tags': body.tags,
    })
    db.commit()
    return True


@router.get(
    "/{post_id}",
    response_model=Post,
    summary='Returns the post'
)
def get_post(post_id: int, db=Depends(get_db)):
    return db.query(PostModel).filter(PostModel.id == post_id).first()
