# from ctypes import Union
from typing import Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException
from .schemas import UserDisplay, Users
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from routers.schemas import UserBase

router = APIRouter(
    prefix='/users',
    tags=["users"]
)

Users.update_forward_refs()
@router.post('', response_model=Union[UserDisplay,Dict])
async def create_user(request: UserBase, db: Session = Depends(get_db)):
    try:
        val = db_user.get_user_by_username(db, request.username)
        return {'success': False, 'detail': 'username already exists'}
    except HTTPException:
        try:
            return {'success': True, 'detail': db_user.create_user(db, request)}
        except Exception:
            return {'success': False, 'detail': 'Error occurred while adding user due to: ' + str(Exception.__cause__)}


@router.get('/all',response_model=List[Users])
async def get_all_user(db: Session = Depends(get_db)):
    users = db_user.get_all_users(db)
    if len(users) < 1:
        return {'success': False, 'detail': 'No users exist'}
    else:
        return users
        # return [ Users(id=users[2].id,email=users[2].email,username=users[2].username,followers=users[2].followers) ]

@router.get('/user/{username}',response_model=Users)
async def get_user_by_username(username:str, db: Session = Depends(get_db)):
    user = db_user.get_user_by_username(db,username)
    if not user:
        return {'success': False, 'detail':f'user with{username} doesnot exist'}
    else:
        return user
    

@router.post('/add-follower')
async def add_following(db: Session = Depends(get_db), username:str = None, following:str= None):
    if not username or not following:
        return {'success': False, 'detail': 'Query params cannot be empty'}

    try:
        user = db_user.add_follower(db, username, following)
        return {'success': True, 'detail': 'Added user Successfully', 'user':user}
    except Exception as exp:
        return {'success': False, 'detail': "Couldn't add follower due to: " + str(exp.__cause__)}
