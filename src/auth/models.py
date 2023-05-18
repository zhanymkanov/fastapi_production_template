from sqlalchemy.orm import mapped_column
from sqlalchemy import Boolean, String
from src.database import Base


class User(Base):
    __tablename__ = "users"

    first_name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)
    username = mapped_column(String, unique=True, nullable=False)
    email = mapped_column(String, unique=True, nullable=False)
    is_admin = mapped_column(Boolean, default=False, nullable=False)
    password = mapped_column(String, nullable=False)
