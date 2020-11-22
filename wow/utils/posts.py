#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from typing import Optional

from sqlalchemy import desc

from blizzard.core import blizzard_db
from database import DatabaseUtils
from database.wow.models import PostCategoryModel, PostModel, PostCommentsModel, PostLikeModel


class PostsUtils:

    @staticmethod
    def add_category(user_id, title, url):
        """
        Adds the comment
        :param user_id:
        :param title:
        :param url:
        :return:
        """
        db = blizzard_db()
        return DatabaseUtils.insert(db, PostCategoryModel(
            title=title,
            user_id=user_id,
            url=url,
        ))

    @staticmethod
    def add_comment(user_id, post_id: int, text: str, reply_id: Optional[int] = None):
        """
        adds the comment

        :param user_id:
        :param post_id:
        :param text:
        :param reply_id:
        :return:
        """
        db = blizzard_db()
        return DatabaseUtils.insert(
            db,
            PostCommentsModel(
                user_id=user_id,
                post_id=post_id,
                reply_id=reply_id if reply_id is not None else 0,
                text=text
            )
        )

    @staticmethod
    def add_like(user_id: int, post_id: int):
        """
        Adds like
        :param user_id:
        :param post_id:
        :return:
        """
        db = blizzard_db()
        val = db.query(PostLikeModel) \
            .filter(PostLikeModel.user_id == user_id) \
            .filter(PostLikeModel.post_id == post_id).count()
        if val == 0:
            DatabaseUtils.insert(
                db,
                PostLikeModel(
                    post_id=post_id,
                    user_id=user_id,
                )
            )
            return True
        else:
            return False

    @staticmethod
    def remove_like(user_id: int, post_id: int):
        """
        Removes like
        :param user_id:
        :param post_id:
        :return:
        """
        db = blizzard_db()
        db.query(PostLikeModel) \
            .filter(PostLikeModel.user_id == user_id) \
            .filter(PostLikeModel.post_id == post_id).delete()
        db.commit()
        return db

    @staticmethod
    def add_post(user_id: int, category_id: int, title: str, content: str, image: str, tags: str):
        db = blizzard_db()
        return DatabaseUtils.insert(db, PostModel(
            user_id=user_id,
            category_id=category_id,

            title=title,
            content=content,
            tags=tags,

            image=image,
        ))

    @staticmethod
    def get_categories():
        """
        Returns the categories
        :return:
        """
        db = blizzard_db()
        return DatabaseUtils.core_query(db.query(PostCategoryModel)).all()

    @staticmethod
    def get_posts_limit(offset: int = 0, limit: int = 100):
        """
        Returns the posts by limit
        :param offset:
        :param limit:
        :return:
        """
        db = blizzard_db()
        return DatabaseUtils.limited_results_query(db.query(PostModel).order_by(PostModel.id.desc()), offset=offset, limit=limit)

    @staticmethod
    def get_posts_by_category_limit(category_id: int, offset: int = 0, limit: int = 100):
        """
        Returns the posts by category id

        :param category_id:
        :param offset:
        :param limit:
        :return:
        """
        db = blizzard_db()
        return DatabaseUtils.limited_results_query(
            db.query(PostModel).filter(PostModel.category_id == category_id).order_by(desc(PostModel.id)),
            offset=offset,
            limit=limit
        )
