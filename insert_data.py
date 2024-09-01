import sqlite3

def addAdmin(telegram_id):
    try:
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO admins (telegram_id) VALUES (?)"""

        cursor.execute(sqlite_insert_query, (telegram_id,))
        sqliteConnection.commit()
        print("Record inserted successfully into admins table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            
def deleteAdmin(telegram_id):
    try:
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_delete_query = """DELETE FROM admins WHERE telegram_id = ?"""

        cursor.execute(sqlite_delete_query, (telegram_id,))
        sqliteConnection.commit()
        print("Record deleted successfully from admins table", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def fetchAllAdmins():
    records = []
    try:
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_select_query = """SELECT * FROM admins"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Records fetched successfully from admins table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to fetch data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return records

def add_data(telegram_id, username, phone_number=None, is_premium=False):
    try:
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        if phone_number is None:
            insert_query = '''INSERT INTO users (telegram_id, username)
                              VALUES (?, ?);'''
            data = (telegram_id, username)
        else:
            insert_query = '''INSERT INTO users (telegram_id, username, phone_number, is_premium)
                              VALUES (?, ?, ?, ?);'''
            data = (telegram_id, username, phone_number, is_premium)

        cursor.execute(insert_query, data)

        sqliteConnection.commit()
        print("Record inserted successfully")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite connection is closed")

def update_phone_number(telegram_id, phone_number):
    conn = sqlite3.connect('users.db') 
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users
        SET phone_number = ?
        WHERE telegram_id = ?
    """, (phone_number, telegram_id))
    
    conn.commit()
    conn.close()