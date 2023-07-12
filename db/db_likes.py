from datetime import datetime
from sqlalchemy.orm import Session

from routers.schemas import PostLikeBase
from db.models import DbPostLikes


def create(db: Session, request: PostLikeBase):
  new_like = DbPostLikes(
    likeid = request.Likeid,
    username=request.username,
    post_id=request.post_id
  )

  db.add(new_like)
  db.commit()
  db.refresh(new_like)
  return new_like

def get_all(db: Session, post_id: int):
   return db.query(DbPostLikes).filter(DbPostLikes.post_id == post_id).all()


#   new_comment = DbComment(
#     text = request.text,
#     username = request.username,
#     post_id = request.post_id,
#     timestamp = datetime.now()
#   )
#   db.add(new_comment)
#   db.commit()
#   db.refresh(new_comment)
#   return new_comment
