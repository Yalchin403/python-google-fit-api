from sqlalchemy import Column, String, Boolean, DateTime, Integer
from passlib.hash import bcrypt
from apps.utils.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    username = Column(String(100), unique=False, nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    password = Column(String(128), nullable=True)
    date_joined = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)
    image = Column(String, nullable=True)

    def set_password(self, password: str) -> None:
        self.password = bcrypt.hash(password)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)

    def verify_user(self) -> None:
        if not self.is_verified:
            self.is_verified = True

    def __str__(self) -> str:
        return f"{self.email}-{self.status}"

    def save(self):
        self.set_password(self.password)
        super().save()
