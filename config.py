BOT_TOKEN = "7249637848:AAH9ygCazVHZlQypM9UlJSFJ6iiKuNHNRwM"
OTDB_API_URL = "https://opentdb.com/api.php"
ADMINS = []
MAIN_ADMIN = 5401529389

from insert_data import fetchAllAdmins
admins = fetchAllAdmins()
for admin in admins:
    ADMINS.append(int(admin[0]))
