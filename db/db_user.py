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
        password=Hash.bcrypt(request.password),
        public=bool(request.public),
        db=request.dp)

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

def get_user_by_username_wrt_current_user(db: Session, username: str, current_user:str):
    users: List[DbUser] = db.query(DbUser).filter(DbUser.username.in_((username, current_user))).all()
    if len(users) == 0:
        raise Exception("Incorrect usernames passed")
    elif len(users) == 1:
        if users[0].username == username:
            username = current_user
        else:
            username = username
        raise Exception("Username not found: " + username)

    if users[0].username == username:
        username = users[0]
        current_user = users[1]
    else:
        username = users[1]
        current_user = users[0]

    user = db.query(DbFollowers).filter(DbFollowers.user_id ==username.id,DbFollowers.follower_id == current_user.id).first()

    if not user:
        return username,0
    return username,1


def get_all_users(db: Session):
    users = db.query(DbUser).all()
    # .options(
    #         subqueryload(DbUser.followers),
    #         subqueryload(DbUser.followings))
    return users



def add_follower(db:Session, user:str,follower:str):
    users :List[DbUser] = db.query(DbUser).filter(DbUser.username.in_((user,follower))).all()

    if len(users) == 0:
        raise Exception("Incorrect usernames passed")
    elif len(users) == 1:
        if users[0].username == user:
            not_found = follower
        else:
            not_found = user
        raise Exception("Username not found: " + not_found)

    if users[0].username == user:
        user = users[0]
        follower = users[1]
    else:
        user = users[1]
        follower = users[0]

    add_fw = DbFollowers(user_id=user.id,follower_id=follower.id)
    db.add(add_fw)
    db.commit()
    db.refresh(user)
    return user

def remove_follower(db:Session, user:str,unfollower:str):
    users : List[DbUser] = db.query(DbUser).filter(DbUser.username.in_((user,unfollower))).all()
    if len(users)==0:
        raise Exception("Incorrect usernames passed")
    elif len(users)==1:
        if users[0].username == user:
            not_found = unfollower
        else:
            not_found = user
        raise Exception("Username not found: "+ not_found)

    if users[0].username == user:
        user = users[0]
        unfollower = users[1]
    else:
        user = users[1]
        unfollower = users[0]

    rm_foll = db.query(DbFollowers).filter( DbFollowers.user_id == user.id, DbFollowers.follower_id == unfollower.id).\
              delete()
    db.commit()
    if (rm_foll)>0:
      return True
    else:
      return False


def update_profile(db:Session, request:UserBase, user:DbUser):
    if request.newusername:
        newuser = db.query(DbUser.username).filter(DbUser.username == request.newusername).first()
        if newuser:
            raise Exception("Username already taken")
        else:
            user.username = request.newusername
    if request.email:
        user.email = request.email
    if request.public:
        user.public = bool(request.public)
    if request.password:
        user.password = Hash.bcrypt(request.password)
    if request.dp:
        user.dp = request.dp

    db.commit()
    db.refresh(user)

    return user

