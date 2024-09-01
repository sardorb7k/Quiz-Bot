BOT_TOKEN = "7249637848:AAGgZ8Md89cLzYuEuHuAQOKDiyfTJyFT8f4"
OTDB_API_URL = "https://opentdb.com/api.php"
ADMINS = []
MAIN_ADMIN = 5401529389

from insert_data import fetchAllAdmins
admins = fetchAllAdmins()
for admin in admins:
    ADMINS.append(int(admin[0]))
