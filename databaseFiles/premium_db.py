import sqlite3

def upgrade_user_to_premium(user_id):
    try:
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        update_query = """UPDATE users SET is_premium = 1 WHERE telegram_id = ?"""
        cursor.execute(update_query, (user_id,))
        sqliteConnection.commit()
        print("User's premium status updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update user's premium status", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

import sqlite3

def downgrade_user_from_premium(user_id):
    try:
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_update_query = """UPDATE users SET is_premium = 0 WHERE telegram_id = ?"""
        cursor.execute(sqlite_update_query, (user_id,))
        sqliteConnection.commit()

        print(f"User with ID {user_id} has been downgraded from premium.")
        
    except sqlite3.Error as error:
        print("Failed to update user premium status in sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")