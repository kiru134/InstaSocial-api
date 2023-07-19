from db.database import Base
from sqlalchemy.sql.schema import ForeignKey, Table, UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    msg = Column(String, nullable=False)
    time_stamp = Column(DateTime, nullable=False)
    sender_id = Column(String, ForeignKey('user.id'))
    receiver_id = Column(String,  ForeignKey('user.id'))
    code = Column(String)
    sender = relationship('DbUser', backref= backref("sent_msgs",cascade="all, delete-orphan"))
    receiver = relationship('DbUser', backref= backref("received_msgs",cascade="all, delete-orphan"))

class MessageMapper(Base):
    __tablename__ = 'message_mapper'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(String, ForeignKey('user.id'))
    receiver_id = Column(String,  ForeignKey('user.id'))
    code = Column(String, ForeignKey('message.code'))
    msgs = relationship('Message', backref="mapper",cascade="all, delete-orphan")
