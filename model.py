from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  # Assuming you already have a Base from SQLAlchemy declarative base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func


class Domain(Base):
    """
    The Domain class represents a container or group that owns multiple users.
    """
    __tablename__ = "domain"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(1024), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Establish one-to-many relationship with the User class
    users = relationship("User", back_populates="domain", cascade="all, delete-orphan", lazy="select")

    def __repr__(self):
        return f"<Domain(id={self.id}, name={self.name})>"


class User(Base):
    """
    The User class represents users that can belong to a domain.
    Updated to include a foreign key reference to the domain.
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    bio = Column(String(1024), nullable=True)
    avatar_url = Column(String(512), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Foreign key to associate the user with a domain
    domain_id = Column(Integer, ForeignKey("domain.id", ondelete="CASCADE"), nullable=True)

    # Establish the relationship to the Domain class
    domain = relationship("Domain", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
