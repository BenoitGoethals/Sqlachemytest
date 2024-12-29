from sqlalchemy import Column,Integer,String,DateTime,Text

from sqlalchemy.sql import func
from base import Base
class User(Base):
    def __init__(self, username, password, email, first_name=None, last_name=None, bio=None, avatar_url=None):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.avatar_url = avatar_url

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    bio = Column(String(1024))
    avatar_url = Column(String(512))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"