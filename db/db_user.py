from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.models import DbUser
from db.Hash import Hash

def create_user(db:Session,request:UserBase):
    newuser= DbUser(
        username = request.username,
        email=request.email,
        password=Hash.bcrypt(request.password))

    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser