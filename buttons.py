from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Qani ketdik', callback_data="start_quiz"),
        ]
    ]
)

quiz_category = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Sportlar', callback_data="21"),
            InlineKeyboardButton(text='Mifologiya', callback_data="20"),
        ],
        [
            InlineKeyboardButton(text='Geografiya', callback_data="22"),
            InlineKeyboardButton(text='Matematika', callback_data="19"),
        ],
        [
            InlineKeyboardButton(text='Tarix', callback_data="23"),
            InlineKeyboardButton(text='Hayvonlar', callback_data="27"),
        ], 
        [
            InlineKeyboardButton(text='Transportlar', callback_data="28"),
            InlineKeyboardButton(text='Siyosat', callback_data="24"),
        ],
    ]
)

difficulty_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Oson', callback_data="easy"),
            InlineKeyboardButton(text="O'rtacha", callback_data="medium"),
        ],
        [
            InlineKeyboardButton(text='Qiyin', callback_data="hard"),
        ]
    ]
)

types_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ko'p javobli", callback_data="multiple"),
            InlineKeyboardButton(text="Rost yoki yolg'on", callback_data="boolean"),
        ]
    ]
)

buy_premium_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Premium xarid qilish", callback_data="buy_premium")],
    ]
)

restart_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='😁 Yana', callback_data="start_quiz"),
        ]
    ]
)

admin_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Premium foydalanuchilari", callback_data="premium_users"),
            InlineKeyboardButton(text="Bot foydalanuchilari", callback_data="bot_users"),
        ],
        [InlineKeyboardButton(text="Adminlar", callback_data="admins")]
    ]
)

show_admins_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ko'rsatish", callback_data="show_admins"),
        ]
    ]
)

delete_admin_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'chirish", callback_data="delete_admin"),
        ]
    ]
)

premium_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ko'rsatish", callback_data="get_premium_users"),
        ]
    ]
)

def create_show_users_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ko'rsatish", callback_data="show_bot_users")]
        ]
    )

def create_premium_toggle_button(user_id, is_premium):
    if is_premium:
        text = "Premiumdan olish"
        callback_data = f"unmake_premium:{user_id}"
    else:
        text = "Premiumga qo'shish"
        callback_data = f"make_premium:{user_id}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback_data)]
        ]
    )

# Default

share_phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon raqamni jo'natish", request_contact=True)]
    ], resize_keyboard=True
)