from db.database import Base
from sqlalchemy.sql.schema import ForeignKey, Table,UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column

# DbFollowers = Table(
#     'followers', Base.metadata,
#     Column("user_id", Integer, ForeignKey('user.id'), primary_key=True),
#     Column("follower_id", Integer, ForeignKey('user.id'), primary_key=True)
# )


class DbFollowers(Base):
    __tablename__ = 'follow'
    user_id = Column(Integer, ForeignKey('user.id'),primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'),primary_key=True)

class DbUser(Base):
    __tablename__ = 'user'
    id=Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    public = Column(Boolean)
    dp = Column(String,nullable=True)
    __table_args__ = (UniqueConstraint('username', 'email',name="uniquecol"),)
    posts = relationship('DbPost', back_populates='user')
    # following = relationship("DbUser", back_populates="user")
    # follower_id = Column(Integer,ForeignKey('user.id'),nullable=True)
    # followers = relationship('DbUser', backref=backref("parent", remote_side=[id]))
    followers = relationship(
        "DbUser",
        secondary=DbFollowers.__table__,
        primaryjoin=(id == DbFollowers.user_id),
        secondaryjoin=(id == DbFollowers.follower_id),
        # lazy="joined",
        # join_depth=2,
        backref="followings",
    )
  

class DbPost(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    # numLikes=Column(Integer,ForeignKey('Postlikes.post_id'))
    user = relationship('DbUser', back_populates='posts')
    comments = relationship('DbComment', back_populates='post')
    likes = relationship("DbPostLikes", back_populates="post")


class DbPostLikes(Base):
    __tablename__ = "Postlikes"
    likeid = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("DbPost", back_populates="likes")


class DbComment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("DbPost", back_populates="comments")
    likes = relationship("DbCommentLikes", back_populates="comment")


class DbCommentLikes(Base):
    __tablename__ = "Commentlikes"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    comment_id = Column(Integer, ForeignKey('comment.id'))
    comment = relationship("DbComment", back_populates="likes")
