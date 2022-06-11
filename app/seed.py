from contextlib import closing
import sqlite3


if __name__ == "__main__":
    with closing(sqlite3.connect("flask_tut.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                """INSERT INTO users (username, password, favourite_color) VALUES
                ('Gordon', 'Ramsay', 'red'),
                ('Ironman', 'Tony', 'pink'),
                ('Spiderman', 'Peter', 'red'),
                ('Black Panter', 'Wakanda', 'black'),
                ('Thor', 'Thor', 'purple');
                """
            )
            cursor.execute(
                """INSERT INTO colors (color) VALUES 
                ('blue'), 
                ('indigo'),
                ('purple'),
                ('pink'),
                ('red'),
                ('orange'),
                ('yellow'),
                ('green'),
                ('teal'),
                ('cyan'),
                ('gray'),
                ('black'),
                ('white');
                """
            )
            connection.commit()
