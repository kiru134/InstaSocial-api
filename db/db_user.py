from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only, subqueryload

from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.models import DbUser, DbFollowers
from db.Hash import Hash
from fastapi import HTTPException, status


def create_user(db: Session, request: UserBase):
    newuser = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password))

    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    return user


def get_all_users(db: Session):
    users = db.query(DbUser).all()
    # .options(
    #         subqueryload(DbUser.followers),
    #         subqueryload(DbUser.followings))
    return users



def add_follower(db:Session, user:str,followed_by:str):
    users :List[DbUser] = db.query(DbUser).filter(DbUser.username.in_((user,followed_by))).all()
    if users[0].username == user:
        user = users[0]
        followed_by = users[1]
    else:
        user = users[1]
        followed_by = users[0]

    # if type(user.followers) == List:
    #     user.followers.append(followed_by)
    # else:
    #     user.followers = [followed_by]
    add_fw = DbFollowers(user_id=user.id,follower_id=followed_by.id)
    # add_following = DbFollowing(user_id=followed_by.id,following_id=user.id)
    db.add(add_fw)
    # db.add(add_following)
    db.commit()
    db.refresh(user)
    return user





