from typing import Optional
from contextlib import closing
import sqlite3


DATABASE_NAME = "flask_tut.db"


def get_color_for_user(username: str) -> Optional[str]:
    """Select user's favourite color from `users` table."""
    with closing(sqlite3.connect(DATABASE_NAME, check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"SELECT favourite_color FROM users WHERE username='{username}' ORDER BY pk;")
            result = cursor.fetchone()
            return result[0] if result else None


def get_all_colors():
    """Select all available colors from `colors` table."""
    with closing(sqlite3.connect(DATABASE_NAME, check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"SELECT color FROM colors WHERE is_active=1 ORDER BY pk;")
            colors = cursor.fetchall()
            yield from map(lambda color: color[0], colors)


def check_color_exists(color: str) -> bool:
    """Check that `color` is presented in `colors` table."""
    with closing(sqlite3.connect(DATABASE_NAME, check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"SELECT color FROM colors WHERE is_active=1 AND color='{color}' ORDER BY pk;")
            result = cursor.fetchone()
            return True if result else False


def check_user_exists(username: str, password: str) -> bool:
    """Check that user with `username` and `password` is presented in `users` table."""
    with closing(sqlite3.connect(DATABASE_NAME, check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"SELECT pk FROM users WHERE username='{username}' AND password='{password}' "
                           "ORDER BY pk;")
            result = cursor.fetchone()
            return True if result else False


def check_username_exists(username: str) -> bool:
    """Check that `username` is presented in `users` table."""
    with closing(sqlite3.connect(DATABASE_NAME, check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"SELECT pk FROM users WHERE username='{username}' ORDER BY pk;")
            result = cursor.fetchone()
            return True if result else False


def signup(username: str, password: str, favourite_color: str) -> bool:
    """Insert new record into `users` table if `username` is not already presented in `users` table."""
    with closing(sqlite3.connect(DATABASE_NAME, check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            if check_username_exists(username=username) is False:
                cursor.execute("INSERT INTO users (username, password, favourite_color) VALUES "
                               f"('{username}', '{password}', '{favourite_color}');")
                connection.commit()
                return True  # User signed up.

            return False  # User already exists.
