from datetime import datetime
from sqlalchemy.orm import Session
from db.models import DbComment, DbUser
from routers.schemas import CommentBase, RemoveComment


def create(db: Session, request: CommentBase):

  if not db.query(DbUser).filter(DbUser.id==request.user_id).first():
     raise Exception("User doesn't exist")

  new_comment = DbComment(
    text = request.text,
    user_id = request.user_id,
    post_id = request.post_id,
    timestamp = datetime.now()
  )
  db.add(new_comment)
  db.commit()
  db.refresh(new_comment)
  return new_comment

def remove(db: Session, request: RemoveComment):
  comment = db.query(DbComment).filter(DbComment.id==request.id).delete()
  if not comment:
      raise Exception("Comment not found")

  db.commit()
  return



def get_all(db: Session, post_id: int,limit:int,page:int):
  skip = limit * page - limit
  return db.query(DbComment).filter(DbComment.post_id == post_id).limit(limit).offset(skip).all()