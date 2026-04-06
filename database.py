import sqlite3

CREATE_GAMES_TABLE = "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, name TEXT, platform TEXT, rating INTEGER);"

INSERT_GAME = "INSERT INTO games (name, platform, rating) VALUES (?, ?, ?);"
 
GET_ALL_GAMES = "SELECT * FROM games;"
GET_GAMES_BY_NAME = "SELECT * FROM games WHERE name = ?;"
GET_BEST_PLATFORM_FOR_GAME = """
SELECT * FROM games
WHERE name = ?
ORDER BY rating DESC
LIMIT 1;"""