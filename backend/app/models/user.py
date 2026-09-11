from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, index=True, nullable=False)

    email = Column(String(100), unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    full_name = Column(String(100), nullable=True)

    role = Column(String(50), nullable=False, default="user")

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    is_active = Column(Boolean, default=True)