from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from routers.schemas import PostLikeBase
from db.models import DbPostLikes, DbUser, DbPost


def create(db: Session, request: PostLikeBase):
    if db.query(DbPostLikes.post_id).filter(
            and_(DbPostLikes.username == request.username, DbPostLikes.post_id == request.post_id)).first():
        raise Exception('Post already liked by user')

    if not db.query(DbUser).filter(DbUser.username==request.username).first():
        raise Exception('User does not exist')

    if not db.query(DbPost).filter(DbPost.id == request.post_id).first():
        raise Exception('Post does not exist')

    new_like = DbPostLikes(
        username=request.username,
        post_id=request.post_id)

    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


def get_all(db: Session, post_id: int):
    return db.query(DbPostLikes).filter(DbPostLikes.post_id == post_id).all()


def remove_like(db: Session, post_id: int, username: str):
    like = db.query(DbPostLikes).filter(DbPostLikes.post_id == post_id,DbPostLikes.username == username).first()

    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with {username} has not liked the post')

    db.delete(like)
    db.commit()
