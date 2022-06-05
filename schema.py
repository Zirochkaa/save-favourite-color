from contextlib import closing
import sqlite3


if __name__ == "__main__":
    with closing(sqlite3.connect("flask_tut.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    pk INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(16),
                    password VARCHAR(32),
                    favourite_color VARCHAR(32),
                    is_active BOOLEAN NOT NULL CHECK (is_active IN (0, 1)) DEFAULT 1
                );"""
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS colors(
                    pk INTEGER PRIMARY KEY AUTOINCREMENT,
                    color VARCHAR(16),
                    is_active BOOLEAN NOT NULL CHECK (is_active IN (0, 1)) DEFAULT 1
                );"""
            )
            connection.commit()
