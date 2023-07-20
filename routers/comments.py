from typing import List

from routers.schemas import CommentBase, UserAuth, RemoveComment, Comment
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_comment
from auth.oAuth2 import get_current_user

router = APIRouter(
  prefix='/comment',
  tags=['comment']
)

@router.get('/all/{post_id}',response_model=List[Comment])
def comments(post_id: int, limit:int=10, page:int= 1, db: Session = Depends(get_db)):
  return db_comment.get_all(db, post_id,limit,page)


@router.post('/add')
def create(request: CommentBase, db: Session = Depends(get_db)):
  try:
    return db_comment.create(db, request)
  except Exception as e:
    return {'success': False, 'detail': "Couldn't add comment: " + str(e)}

@router.delete('/delete')
def create(request: RemoveComment, db: Session = Depends(get_db)):
  try:
    db_comment.remove(db, request)
    return {'success': True, 'detail': "Removed Comment"}
  except Exception as e:
    return {'success': False, 'detail': "Couldn't remove comment: " + str(e)}