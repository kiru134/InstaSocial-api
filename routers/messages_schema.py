from pydantic import BaseModel


class MessageRequest(BaseModel):
    sender_id:str
    receiver_id:str
    msg:str

class MessageMapperRequest(BaseModel):
    sender_id:str
    receiver_id:str
    msg:str