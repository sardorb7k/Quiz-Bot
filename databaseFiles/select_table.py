import sqlite3

def readSqliteTable(premium=False):
    records = []
    try:
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        if premium:
            sqlite_select_query = """SELECT * FROM users WHERE is_premium = TRUE"""
        else:
            sqlite_select_query = """SELECT * FROM users"""

        cursor.execute(sqlite_select_query)
        records = cursor.fetchall() 
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return records