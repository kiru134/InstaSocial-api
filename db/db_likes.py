from datetime import datetime
from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from routers.schemas import PostLikeBase
from db.models import DbPostLikes


def create(db: Session, request: PostLikeBase):
  new_like = DbPostLikes(
    username=request.username,
    post_id=request.post_id
  )

  db.add(new_like)
  db.commit()
  db.refresh(new_like)
  return new_like

def get_all(db: Session, post_id: int):
   return db.query(DbPostLikes).filter(DbPostLikes.post_id == post_id).all()

def removelike(db:Session,post_id: int,username:str):
  like = db.query(DbPostLikes).filter(DbPostLikes.post_id == post_id and DbPostLikes.username==username).delete(synchronize_session=False)
  # if not like:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
  #         detail=f'Post with id {id} not found')
  if not like:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail= f'user with {username} has not liked the post')

  db.delete(like)
  db.commit()
  return 'ok'
   
