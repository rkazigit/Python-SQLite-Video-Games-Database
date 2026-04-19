import sqlite3

CREATE_GAMES_TABLE = "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, name TEXT, platform TEXT, rating INTEGER);"
CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT);"

INSERT_GAME = "INSERT INTO games (name, platform, rating) VALUES (?, ?, ?);"
INSERT_USER = "INSERT INTO users (username, password) VALUES (?, ?);"

GET_ALL_GAMES = "SELECT * FROM games;"
GET_GAMES_BY_NAME = "SELECT * FROM games WHERE name = ?;"
GET_GAMES_BY_RATING_RANGE = "SELECT * FROM games WHERE rating BETWEEN ? AND ? ORDER BY rating DESC;"
GET_BEST_PLATFORM_FOR_GAME = """
SELECT * FROM games
WHERE name = ?
ORDER BY rating DESC
LIMIT 1;"""

DELETE_GAME_BY_NAME = "DELETE FROM games WHERE name = ?;"
DELETE_GAME_BY_ID = "DELETE FROM games WHERE id = ?;"

GET_USER = "SELECT * FROM users WHERE username = ? AND password = ?;"
GET_USER_BY_USERNAME = "SELECT * FROM users WHERE username = ?;"


def connect():
    return sqlite3.connect("data.db")
 
def create_tables(connection):
    with connection:
        connection.execute(CREATE_GAMES_TABLE)
        connection.execute(CREATE_USERS_TABLE)

def add_game(connection, name, platform, rating):
    with connection:
        connection.execute(INSERT_GAME, (name, platform, rating))
 
def get_all_games(connection):
    with connection:
        return connection.execute(GET_ALL_GAMES).fetchall()
 
def get_games_by_name(connection, name):
    with connection:
        return connection.execute(GET_GAMES_BY_NAME, (name,)).fetchall()
 
def get_best_platform_for_game(connection, name):
    with connection:
        return connection.execute(GET_BEST_PLATFORM_FOR_GAME, (name,)).fetchone()
    
def delete_game_by_name(connection, name):
    with connection:
        cursor = connection.execute(DELETE_GAME_BY_NAME, (name,))
        return cursor.rowcount  # number of rows deleted

def delete_game_by_id(connection, game_id):
    with connection:
        cursor = connection.execute(DELETE_GAME_BY_ID, (game_id,))
        return cursor.rowcount

#user/password


def add_user(connection, username, password):
    
    try:
        with connection:
            connection.execute(INSERT_USER, (username, password))
        return True
    except sqlite3.IntegrityError:
        return False
 
 
def get_user(connection, username, password):
    with connection:
        return connection.execute(GET_USER, (username, password)).fetchone()
 
 
def username_exists(connection, username):
    with connection:
        return connection.execute(GET_USER_BY_USERNAME, (username,)).fetchone() is not None