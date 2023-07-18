from __future__ import annotations
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, ForwardRef, Optional

from routers.validators import string_must_contain_letter


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    password: Optional[str] = None
    public: Optional[int] = 0
    dp: Optional[str] = None
    newusername: Optional[str] = None


class UserAuth(BaseModel):
    id: int
    username: str
    email: str


class UserDisplay(BaseModel):
    username: str
    email: str

    class Config():
        orm_mode = True


class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int

    img_validator = field_validator('image_url')(string_must_contain_letter)


# For PostDisplay
class User(BaseModel):
    username: str
    id: int
    public: bool
    dp: Optional[str]

    class Config():
        from_attributes = True
        orm_mode = True


# For PostDisplay
class Comment(BaseModel):
    text: str
    user : User
    timestamp: datetime
    likes: List [ CommentLike ]

    class Config():
        from_attributes = True
        orm_mode = True


# To display Likes
class Like(BaseModel):
    username: str
    post_id: int

    class Config():
        from_attributes = True
        orm_mode = True


class PostLikeBase(BaseModel):
    username: str
    post_id: int

class CommentLike(BaseModel):
    username: str
    comment_id: int


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: User
    comments: List[Comment]
    likes: List[Like]

    class Config():
        from_attributes = True
        orm_mode = True


class CommentBase(BaseModel):
    user_id: int
    text: str
    post_id: int

class RemoveComment(BaseModel):
    id: int

# User.update_forward_refs()

class Users(BaseModel):
    id: int
    username: str
    email: str
    public: bool
    dp: Optional[str]
    followers: List[User]
    followings: List[User]
    posts: List[PostDisplay]

    class Config():
        from_attributes = True
        orm_mode = True
