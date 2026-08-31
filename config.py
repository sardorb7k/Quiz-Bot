BOT_TOKEN = "8890832189:AAFWuz8E3QOm9yB2qSpxbeRTc8gYtyK4vj0"
OTDB_API_URL = "https://opentdb.com/api.php"
ADMINS = []
MAIN_ADMIN = 5401529389

from insert_data import fetchAllAdmins
admins = fetchAllAdmins()
for admin in admins:
    ADMINS.append(int(admin[0]))
