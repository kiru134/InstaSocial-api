from routers.messages_schema import MessageRequest
from routers.schemas import CommentBase, UserAuth, RemoveComment
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_comment
from auth.oAuth2 import get_current_user

router = APIRouter(
  prefix='/message',
  tags=['Message']
)

@router.post("/send")
async def add_message(request:MessageRequest):
     pass