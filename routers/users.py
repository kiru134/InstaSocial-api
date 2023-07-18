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


@router.post('/add', response_model=Union[UserDisplay, Dict])
async def create_user(request: UserBase, db: Session = Depends(get_db)):
    try:
        val = db_user.get_user_by_username(db, request.username)
        return {'success': False, 'detail': 'username already exists'}
    except HTTPException:
        try:
            return db_user.create_user(db, request)
        except Exception as e:
            return {'success': False, 'detail': 'Error occurred while adding user due to: ' + str(e)}


@router.post('/update', response_model=Union[UserDisplay, Dict])
async def update_user(request: UserBase, db: Session = Depends(get_db)):
    try:
        user = db_user.get_user_by_username(db, request.username)
        if not user:
            return {'success': False, 'detail': 'username does not exist'}
        else:
            return db_user.update_profile(db, request, user)
    except Exception as e:
        return {'success': False, 'detail': 'Error occurred while modifying user due to: ' + str(e)}


@router.get('/all', response_model=Union[List[Users], Dict])
async def get_all_user(db: Session = Depends(get_db)):
    users = db_user.get_all_users(db)
    if len(users) < 1:
        return {'success': False, 'detail': 'No users exist'}
    else:
        return users
        # return [ Users(id=users[2].id,email=users[2].email,username=users[2].username,followers=users[2].followers) ]


@router.get('/user/{username}', response_model=Users)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db_user.get_user_by_username(db, username)
    if not user:
        return {'success': False, 'detail': f'user with{username} does not exist'}
    else:
        return user

@router.get('/user', response_model=Dict)
async def get_user_by_username_wrt_current_user(username: str, current_user:str, db: Session = Depends(get_db)):
        user,status = db_user.get_user_by_username_wrt_current_user(db, username, current_user)
        if status:
            return {'success': True, 'detail': "Success",'user':Users.from_orm(user) }
        else:
            return {'success': False,'detail':f'{username} is not followed by current user:{current_user}' ,'user':Users.from_orm(user)}

@router.post('/add-follower')
async def add_following(db: Session = Depends(get_db), username: str = None, follower: str = None):
    if not username or not follower:
        return {'success': False, 'detail': 'Query params cannot be empty'}
    try:
        user = db_user.add_follower(db, username, follower)
        return {'success': True, 'detail': 'Added user Successfully', 'user': user}
    except Exception as exp:
        return {'success': False, 'detail': "Couldn't add follower due to: " + str(exp)}


@router.delete('/remove-follower', response_model=Dict)
async def remove_following(db: Session = Depends(get_db), username: str = None, follower: str = None):
    if not username or not follower:
        return {'success': False, 'detail': 'Query params cannot be empty'}
    try:
        status = db_user.remove_follower(db, username, follower)
        if status:
            return {'success': True, 'detail': 'Removed follower Successfully', 'user': follower}
        else:
            return {'success': False, 'detail': f"Couldn't remove follower since {follower} doesn't follow {username} "}
    except Exception as exp:
        return {'success': False, 'detail': "Couldn't remove follower due to: " + str(exp)}
