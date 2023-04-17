from __future__ import annotations

import random
from typing import Optional, List
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class Color(db.Model):
    __tablename__ = "colors"

    color = db.Column(db.String(20), primary_key=True, index=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    users = db.relationship("User", backref="colors_lol")

    def __repr__(self):  # pragma: no cover
        return f"Color(color='{self.color}', is_active={self.is_active})"

    def __str__(self):  # pragma: no cover
        return self.color

    # __repr__ = __str__

    @classmethod
    def check_exists(cls, color: str) -> Optional[Color]:
        return cls.query.filter(cls.is_active.is_(True), cls.color == color).first()

    @classmethod
    def get_all_active_colors(cls) -> List[Color]:
        return cls.query.filter(cls.is_active.is_(True)).order_by(cls.color.asc()).all()

    @classmethod
    def get_all_colors(cls) -> List[Color]:
        return cls.query.order_by(cls.color.asc()).all()

    @classmethod
    def get_random_color(cls, only_active: bool = True) -> Optional[Color]:
        query = cls.query

        if only_active is True:
            query = query.filter(cls.is_active.is_(True))

        all_colors = query.all()
        return random.choice(all_colors) if all_colors else None


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password = db.Column(db.String(102), nullable=False)
    favourite_color = db.Column(db.String(20), ForeignKey("colors.color"))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(
        self,
        username: str,
        password: str,
        favourite_color: str,
        is_active: bool = True,
        is_admin: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.username = username
        self.password = generate_password_hash(password)
        self.favourite_color = favourite_color
        self.is_active = is_active
        self.is_admin = is_admin

    def __repr__(self):  # pragma: no cover
        return f"User(id={self.id}, username='{self.username}', favourite_color='{self.favourite_color}', " \
               f"is_active={self.is_active}, is_admin={self.is_admin}, " \
               f"is_authenticated={self.is_authenticated}, is_anonymous={self.is_anonymous})"

    def __str__(self):  # pragma: no cover
        return self.username

    def get_id(self) -> int:
        return self.id

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def save_favourite_color(self, favourite_color: str):
        self.favourite_color = favourite_color
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_random_user(cls, only_active: bool = True) -> Optional[User]:
        """
        Returns random user which is not an admin.
        """
        query = cls.query.filter(cls.is_admin.is_(False))

        if only_active is True:
            query = query.filter(cls.is_active.is_(True))

        all_users = query.all()
        return random.choice(all_users) if all_users else None

    @classmethod
    def signup(cls, username: str, password: str, favourite_color: str) -> User:
        """
        Creates new user in db.
        """
        user = cls(username=username, password=password, favourite_color=favourite_color)
        db.session.add(user)
        db.session.commit()
        return user
