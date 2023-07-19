from fastapi import HTTPException, status
from sqlalchemy import or_, and_, desc
from sqlalchemy.testing import in_

from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import DbPost, DbUser, DbFollowers
import datetime


def create(db: Session, request: PostBase):
    new_post = DbPost(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.datetime.now(),
        user_id=request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all(db: Session):
    return db.query(DbPost).all()


def get_userpost(user_name: str, db: Session):
    posts = db.query(DbPost).filter(and_(DbPost.user_id == DbUser.id, DbUser.username == user_name)).order_by( desc(DbPost.timestamp)).all()
    if posts != None:
        return posts
    else:
        return []


def delete(db: Session, id: int, user_id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only post creator can delete post')

    db.delete(post)
    db.commit()
    return 'ok'


def get_postfeed_for_user(db: Session, username: str):
    followings = db.query(DbFollowers.user_id).where(DbFollowers.follower_id == DbUser.id).filter(
        username == DbUser.username)
    posts = db.query(DbPost).where(DbPost.user_id == DbUser.id).filter(
        or_(and_(DbUser.public == True, DbUser.username != username),
            DbPost.user_id.in_(followings.subquery()))).order_by(
        desc(DbPost.timestamp)
    )
    if posts:
        return posts
    else:
        return []
