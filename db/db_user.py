from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.models import DbUser
from db.Hash import Hash
from fastapi import HTTPException, status

def create_user(db:Session,request:UserBase):
    newuser= DbUser(
        username = request.username,
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