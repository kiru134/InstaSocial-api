from fastapi import HTTPException

from routers.schemas import PostLikeBase, UserAuth
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_likes
from auth.oAuth2 import get_current_user

router = APIRouter(
    prefix='/post/likes',
    tags=['Post Likes']
)


@router.get('/all/{post_id}')
def getlikes(post_id: int, db: Session = Depends(get_db)):
    return db_likes.get_all(db, post_id)


@router.delete('/remove')
def remove_likes(request:PostLikeBase, db: Session = Depends(get_db)):
    try:
        db_likes.remove_like(db, request.post_id, request.username)
        return {'success': True, 'detail': "Removed Like"}

    except HTTPException as hx:
        return hx
    except Exception as e:
        return {'success': False, 'detail': "Couldn't remove like due to: " + str(e)}


@router.post('/add')
def add_like(request: PostLikeBase, db: Session = Depends(get_db)):
    try:
        return db_likes.create(db, request)

    except Exception as e:
        return {'success': False, 'detail': "Couldn't add like due to: " + str(e)}
