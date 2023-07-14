from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from routers.schemas import PostLikeBase, CommentLike
from db.models import DbPostLikes, DbUser, DbCommentLikes, DbComment


def add_comment_like(db: Session, request: CommentLike):
    if db.query(DbCommentLikes.comment_id).filter(
            and_(DbCommentLikes.username == request.username, DbCommentLikes.comment_id == request.comment_id)).first():
        raise Exception('Comment already liked by user')

    if not db.query(DbUser).filter(DbUser.username==request.username).first():
        raise Exception('User does not exist')
    if not db.query(DbComment).filter(DbComment.id == request.comment_id).first():
        raise Exception('Comment does not exist')
    new_comment_like = DbCommentLikes(
        username=request.username,
        comment_id=request.comment_id)

    db.add(new_comment_like)
    db.commit()
    db.refresh(new_comment_like)
    return new_comment_like


def get_all_comment_likes(db: Session, comment_id: int):
    return db.query(DbCommentLikes).filter(DbCommentLikes.comment_id == comment_id).all()


def remove_comment_like(db: Session, comment_id: int, username: str):
    like = db.query(DbCommentLikes).filter(DbCommentLikes.comment_id == comment_id,DbCommentLikes.username == username).first()

    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with {username} has not liked the comment or comment doesn"t exist')

    db.delete(like)
    db.commit()
