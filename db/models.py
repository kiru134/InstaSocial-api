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
    __table_args__ = (UniqueConstraint('username', 'email', name="uniquecol"),)
    id=Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    public = Column(Boolean)
    dp = Column(String,nullable=True)
    posts = relationship('DbPost', order_by="desc(DbPost.timestamp)", back_populates='user', cascade="all, delete-orphan")
    comments = relationship('DbComment',back_populates='user',cascade="all, delete-orphan")
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
    user_id = Column(Integer, ForeignKey('user.id',ondelete='CASCADE'))
    user = relationship('DbUser', back_populates='posts')
    comments = relationship('DbComment', order_by="desc(DbComment.timestamp)", back_populates='post', cascade="all,delete",passive_deletes=True)
    likes = relationship("DbPostLikes", back_populates="post", cascade="all,delete",passive_deletes=True)


class DbPostLikes(Base):
    __tablename__ = "Postlikes"
    likeid = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    post_id = Column(Integer, ForeignKey('post.id',ondelete='CASCADE'))
    post = relationship("DbPost", back_populates="likes")
    __table_args__ = ( UniqueConstraint('username', 'post_id', name="uniquepostlikes"),)


class DbComment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    user_id = Column(Integer,ForeignKey('user.id',ondelete='CASCADE'))
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id',ondelete='CASCADE'))
    post = relationship("DbPost", back_populates="comments")
    likes = relationship("DbCommentLikes", back_populates="comment", cascade="all,delete", passive_deletes=True)
    user = relationship("DbUser",uselist=False, back_populates="comments")


class DbCommentLikes(Base):
    __tablename__ = "Commentlikes"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    comment_id = Column(Integer, ForeignKey('comment.id',ondelete='CASCADE'))
    comment = relationship("DbComment", uselist=False, back_populates="likes")
