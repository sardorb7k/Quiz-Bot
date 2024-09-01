import sqlite3

try:
    sqliteConnection = sqlite3.connect('users.db')
    
    sqlite_create_table_query = '''CREATE TABLE admins (
                                telegram_id INTEGER PRIMARY KEY);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("SQLite connection is closed")