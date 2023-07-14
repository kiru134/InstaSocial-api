from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_comment_likes
from db.database import get_db
from routers.schemas import CommentLike

router = APIRouter(
    prefix='/comment/likes',
    tags=['Comment Likes']
)


@router.get('/all/{comment_id}')
def get_comment_likes(comment_id: int, db: Session = Depends(get_db)):
    return db_comment_likes.get_all_comment_likes(db, comment_id)


@router.delete('/remove')
def remove_comment_likes(request: CommentLike, db: Session = Depends(get_db)):
    try:
        db_comment_likes.remove_comment_like(db, request.comment_id, request.username)
        return {'success': True, 'detail': "Removed Comment Like"}
    except HTTPException as hx:
        return hx
    except Exception as e:
        return {'success': False, 'detail': "Couldn't remove like due to: " + str(e)}


@router.post('/add')
def add_comment_like(request: CommentLike, db: Session = Depends(get_db)):
    try:
        return db_comment_likes.add_comment_like(db, request)
    except Exception as e:
        return {'success': False, 'detail': "Couldn't add comment like due to: " + str(e)}
