"""Fill colors and users table with data

Revision ID: c7ac8d1dcffa
Revises: 9ee33baa02ad
Create Date: 2022-06-14 16:48:47.215901

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from app.models import Color, User


# revision identifiers, used by Alembic.
revision = 'c7ac8d1dcffa'
down_revision = '9ee33baa02ad'
branch_labels = None
depends_on = None


def upgrade():
    colors_table = sa.Table(
        "colors",
        sa.MetaData(),
        sa.Column("color", sa.String(20), primary_key=True, index=True),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True)
    )

    op.bulk_insert(
        colors_table,
        [
            {
                "color": "blue", "is_active": True
            },
            {
                "color": "indigo", "is_active": True
            },
            {
                "color": "purple", "is_active": True
            },
            {
                "color": "pink", "is_active": True
            },
            {
                "color": "red", "is_active": True
            },
            {
                "color": "orange", "is_active": True
            },
            {
                "color": "yellow", "is_active": True
            },
            {
                "color": "green", "is_active": True
            },
            {
                "color": "teal", "is_active": True
            },
            {
                "color": "cyan", "is_active": True
            },
            {
                "color": "gray", "is_active": True
            },
            {
                "color": "black", "is_active": True
            },
            {
                "color": "white", "is_active": True
            },
        ]
    )

    users_table = sa.Table(
        "users",
        sa.MetaData(),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(30), unique=True, nullable=False, index=True),
        sa.Column("password", sa.String(102), nullable=False),
        sa.Column("favourite_color", sa.String(20), sa.ForeignKey("colors.color")),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True)
    )

    op.bulk_insert(
        users_table,
        [
            {
                "username": "Gordon",
                "password": generate_password_hash("Ramsay"),
                "favourite_color": "green",
                "is_active": True,
            },
            {
                "username": "Ironman",
                "password": generate_password_hash("Tony"),
                "favourite_color": "pink",
                "is_active": True,
            },
            {
                "username": "Spiderman",
                "password": generate_password_hash("Peter"),
                "favourite_color": "red",
                "is_active": True,
            },
            {
                "username": "Black Panter",
                "password": generate_password_hash("Wakanda"),
                "favourite_color": "black",
                "is_active": True,
            },
            {
                "username": "Nebula",
                "password": generate_password_hash("Thanos"),
                "favourite_color": "blue",
                "is_active": True,
            },
            {
                "username": "Rocket",
                "password": generate_password_hash("Raccoon"),
                "favourite_color": "gray",
                "is_active": True,
            },
            {
                "username": "Moon Knight",
                "password": generate_password_hash("Avatar"),
                "favourite_color": "white",
                "is_active": True,
            },
            {
                "username": "Thor",
                "password": generate_password_hash("Thor"),
                "favourite_color": "purple",
                "is_active": True,
            },
        ]
    )


def downgrade():
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM colors")
