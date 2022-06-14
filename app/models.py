from __future__ import annotations
from typing import Optional, List
from sqlalchemy import ForeignKey
from app import db


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


class User(db.Model):
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

    @classmethod
    def check_exists(cls, username: str, password: str) -> Optional[User]:
        return cls.query.filter(cls.username == username, cls.password == password).first()

    @classmethod
    def check_username_exists(cls, username: str) -> bool:
        return True if cls.query.filter(cls.username == username).first() else False

    @classmethod
    def get_favourite_color(cls, username: str) -> Optional[str]:
        user = cls.query.filter(cls.username == username).first()
        return user.favourite_color if user else None

    @classmethod
    def signup(cls, username: str, password: str, favourite_color: str = "", is_active: bool = True) -> Optional[User]:
        if cls.check_username_exists(username=username):
            return None

        user = cls(username=username, password=password, favourite_color=favourite_color, is_active=is_active)
        db.session.add(user)
        db.session.commit()
        return user
