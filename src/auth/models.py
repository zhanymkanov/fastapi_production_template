from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import (
    Boolean,
    String,
    LargeBinary,
    Integer,
    UUID,
    DateTime,
    ForeignKey
)

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, unique=True, nullable=False)
    is_admin = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    password = mapped_column(LargeBinary, nullable=False)
    tokens = relationship("Token", back_populates="user")


class Token(Base):
    __tablename__ = 'refresh_tokens'

    uuid = mapped_column(UUID, primary_key=True)
    refresh_token = mapped_column(String, nullable=False)
    expires_at = mapped_column(DateTime, nullable=False)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="tokens")
