from routers.schemas import PostLikeBase, UserAuth
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_likes
from auth.oAuth2 import get_current_user

router = APIRouter(
  prefix='/post/likes',
  tags=['Likes']
)

@router.get('/all/{post_id}')
def getlikes(post_id: int, db: Session = Depends(get_db)):
  return db_likes.get_all(db, post_id)

@router.post('/all/{username}/{post_id}')
def removelikes(username:str,post_id: int, db: Session = Depends(get_db)):
  return db_likes.removelike(db, post_id,username)

@router.post('')
def createlike(request: PostLikeBase, db: Session = Depends(get_db)):
  return db_likes.create(db, request)


