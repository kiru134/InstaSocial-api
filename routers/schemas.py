from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import List, ForwardRef, Optional


class UserBase(BaseModel):
    username: str
    email: Optional[str]
    password: Optional[str]
    public: Optional[str]
    dp:Optional[str]


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


# For PostDisplay
class User(BaseModel):
    username: str
    id: int

    class Config():
        orm_mode = True


# For PostDisplay
class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime

    class Config():
        orm_mode = True


# To display Likes
class Like(BaseModel):
    username: str
    post_id: int

    class Config():
        orm_mode = True


class PostLikeBase(BaseModel):
    username: str
    post_id: int


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
        orm_mode = True


class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int


# User.update_forward_refs()

class Users(BaseModel):
    id: int
    username: str
    email: str
    public: bool
    followers: List[User]
    followings: List[User]
    posts: List[PostDisplay]

    class Config():
        orm_mode = True
