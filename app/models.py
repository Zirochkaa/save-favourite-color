from __future__ import annotations
from typing import Optional, List
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from . import db


class Color(db.Model):
    __tablename__ = "colors"

    color = db.Column(db.String(20), primary_key=True, index=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    users = db.relationship("User", backref="colors_lol")

    def __repr__(self):
        return f"Color(color='{self.color}', is_active={self.is_active})"

    def __str__(self):
        return self.color

    # __repr__ = __str__

    @classmethod
    def check_exists(cls, color: str) -> Optional[Color]:
        return cls.query.filter(cls.is_active.is_(True), cls.color == color).first()

    @classmethod
    def get_all_active_colors(cls) -> List[Color]:
        return cls.query.filter(cls.is_active.is_(True)).all()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password = db.Column(db.String(30), nullable=False)
    favourite_color = db.Column(db.String(20), ForeignKey("colors.color"))
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', is_active={self.is_active})"

    def __str__(self):
        return self.username

    def get_id(self) -> int:
        return self.id

    def check_password(self, password: str) -> bool:
        return self.password == password

    @classmethod
    def signup(cls, username: str, password: str, favourite_color: str = "", is_active: bool = True) -> User:
        user = cls(username=username, password=password, favourite_color=favourite_color, is_active=is_active)
        db.session.add(user)
        db.session.commit()
        return user
