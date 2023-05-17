from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
