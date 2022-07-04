"""Fill colors and users table with data

Revision ID: c7ac8d1dcffa
Revises: 9ee33baa02ad
Create Date: 2022-06-14 16:48:47.215901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ac8d1dcffa'
down_revision = '9ee33baa02ad'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """INSERT INTO colors (color, is_active) VALUES
        ('blue', 'true'),
        ('indigo', 'true'),
        ('purple', 'true'),
        ('pink', 'true'),
        ('red', 'true'),
        ('orange', 'true'),
        ('yellow', 'true'),
        ('green', 'true'),
        ('teal', 'true'),
        ('cyan', 'true'),
        ('gray', 'true'),
        ('black', 'true'),
        ('white', 'true');
        """
    )
    op.execute(
        """INSERT INTO users (username, password, favourite_color, is_active) VALUES
            ('Gordon', 'Ramsay', 'green', 'true'),
            ('Ironman', 'Tony', 'pink', 'true'),
            ('Spiderman', 'Peter', 'red', 'true'),
            ('Black Panter', 'Wakanda', 'black', 'true'),
            ('Nebula', 'Thanos', 'blue', 'true'),
            ('Rocket', 'Raccoon', 'gray', 'true'),
            ('Moon Knight', 'Avatar', 'white', 'true'),
            ('Thor', 'Thor', 'purple', 'true');
        """
    )


def downgrade():
    op.execute("DELETE FROM users WHERE username='Gordon'")
    op.execute("DELETE FROM users WHERE username='Ironman'")
    op.execute("DELETE FROM users WHERE username='Spiderman'")
    op.execute("DELETE FROM users WHERE username='Black Panter'")
    op.execute("DELETE FROM users WHERE username='Nebula'")
    op.execute("DELETE FROM users WHERE username='Rocket'")
    op.execute("DELETE FROM users WHERE username='Moon Knight'")
    op.execute("DELETE FROM users WHERE username='Thor'")

    op.execute("DELETE FROM colors WHERE color='blue'")
    op.execute("DELETE FROM colors WHERE color='indigo'")
    op.execute("DELETE FROM colors WHERE color='purple'")
    op.execute("DELETE FROM colors WHERE color='pink'")
    op.execute("DELETE FROM colors WHERE color='red'")
    op.execute("DELETE FROM colors WHERE color='orange'")
    op.execute("DELETE FROM colors WHERE color='yellow'")
    op.execute("DELETE FROM colors WHERE color='green'")
    op.execute("DELETE FROM colors WHERE color='teal'")
    op.execute("DELETE FROM colors WHERE color='cyan'")
    op.execute("DELETE FROM colors WHERE color='gray'")
    op.execute("DELETE FROM colors WHERE color='black'")
    op.execute("DELETE FROM colors WHERE color='white'")
