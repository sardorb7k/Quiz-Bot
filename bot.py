from aiogram.filters import Filter
import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from googletrans import Translator
from states import *
from config import *
from buttons import *
from insert_data import add_data, update_phone_number, addAdmin, deleteAdmin
from databaseFiles.select_table import readSqliteTable
from databaseFiles.premium_db import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

translator = Translator()

telegram_id = None
is_premium = False

def getUsersSub():
    global is_premium
    premium_users = readSqliteTable(premium=True)
    for user in premium_users:
        if telegram_id == user[0]:
            is_premium = True
        else:
            is_premium = False

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global telegram_id
    telegram_id = message.from_user.id
    getUsersSub()
    if telegram_id in ADMINS or telegram_id == MAIN_ADMIN:
        await message.answer_photo(photo="https://cdn.images.express.co.uk/img/dynamic/130/590x/1282929_1.jpg", caption='QuizBotga xush kelibsiz admin! 📢\n', reply_markup=admin_button)
    else:
        username = message.from_user.username if message.from_user.username else "unknown"
        phone_number = ""
        add_data(telegram_id, username, phone_number, is_premium=False)
        text = "QuizBotga xush kelibsiz! 📢\nBu bot yordamida bilimlaringizni sinab ko'ring va yangi narsalarni o'rganing."
        await message.answer_photo(
            photo="https://cdn.images.express.co.uk/img/dynamic/130/590x/1282929_1.jpg",
            caption=text,
            reply_markup=start_button
        )




@dp.callback_query(F.data == 'start_quiz')
async def start(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Start.quiz_category)
    await call.message.answer("Kategoriyalardan birini tanlang.", reply_markup=quiz_category)


@dp.callback_query(F.data.in_(['21', '20', '22', '19', '23', '27', '28', '24']))
async def handle_category_selection(call: types.CallbackQuery, state: FSMContext):
    category_id = call.data
    await state.update_data(selected_category_id=category_id)
    await state.set_state(Start.num_questions)
    await call.message.answer("Savollar sonini kiriting (1-15).")


@dp.message(Start.num_questions)
async def handle_number_of_questions(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        num_questions = int(message.text)

        if num_questions > 15 and not is_premium:
            await message.answer_photo(
                photo="https://www.ixbt.com/img/n1/news/2022/5/2/1_25_large.png",
                caption="Siz 15 ta savoldan ko'proq so'ra olmaysiz. Premium foydalanuvchilar esa 30 savolga ega bo'lishadi."
            )
        else:
            await state.update_data(num_questions=num_questions)
            await message.answer("Qiyinlik darajasini tanlang.", reply_markup=difficulty_button)
            await state.set_state(Start.difficulty)
    else:
        await message.answer("Iltimos, to'g'ri raqam kiriting.")


@dp.callback_query(F.data.in_(['easy', 'medium', 'hard']))
async def handle_difficulty_selection(call: types.CallbackQuery, state: FSMContext):
    difficulty = call.data
    await state.update_data(difficulty=difficulty)
    await state.set_state(Start.type)
    await call.message.answer("Savol turini tanlang.", reply_markup=types_button)


@dp.callback_query(F.data.in_(['multiple', 'boolean']))
async def handle_type_selection(call: types.CallbackQuery, state: FSMContext):
    question_type = call.data
    await state.update_data(type=question_type)
    user_data = await state.get_data()
    questions = await fetch_questions(user_data)

    if not questions:
        await call.message.answer("Savollar topilmadi. Iltimos, qaytadan urinib ko'ring.")
    else:
        await state.update_data(questions=questions, current_question_index=0, correct_answers_count=0)
        caption = "Sizga har bir savol uchun 15 daqiqa vaqt beriladi. Vaqtni uzaytirish uchun premiumga obuna bo'lishingiz kerak.\nOmad! 🍀" if not is_premium else "Siz premiumga obuna bo'lganingiz uchun har bir savol uchun 30 daqiqangiz bor!\nOmad 🍀"
        await call.message.answer_photo(
            photo="https://images.wallpaperscraft.ru/image/single/start_slovo_nadpis_156711_1920x1080.jpg",
            caption=caption
        )
        await display_question(call.message, state)


async def fetch_questions(user_data):
    params = {
        'amount': user_data['num_questions'],
        'category': user_data['selected_category_id'],
        'difficulty': user_data['difficulty'],
        'type': user_data['type']
    }
    response = await asyncio.to_thread(requests.get, OTDB_API_URL, params=params)
    data = response.json()
    return data.get('results', [])


async def display_question(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    question_index = user_data.get('current_question_index', 0)
    
    if question_index < len(user_data['questions']):
        question = user_data['questions'][question_index]
        question_text = f"{question_index + 1}. {question['question']}"
        correct_answer = question['correct_answer']

        options = (['True', 'False'] if user_data['type'] ==
                   'boolean' else question['incorrect_answers'] + [correct_answer])
        import random
        random.shuffle(options)

        sent_message = await send_question(message, question_text, options, correct_answer, question_index + 1)

        await state.update_data(current_message_id=sent_message.message_id)

        wait_time = 30 if is_premium else 15
        await asyncio.sleep(wait_time)

        user_data = await state.get_data()
        if question_index == user_data.get('current_question_index', 0):
            await message.answer("Vaqt tugadi! ⌚")
            await state.update_data(current_question_index=question_index + 1)
            await display_question(message, state)
    else:
        correct_answers_count = user_data.get('correct_answers_count', 0)
        total_questions = user_data.get('num_questions', 0)
        score_message = f"Quiz tugadi! Siz {correct_answers_count} ta to'g'ri javob berdingiz."
        await message.answer_photo(
            photo=f"https://via.placeholder.com/300x200/6495ED/fff?text={correct_answers_count}/{total_questions}",
            caption=score_message,
            reply_markup=restart_button
        )


async def send_question(message: types.Message, question, options, correct_answer, question_number):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=translator.translate(
                option, dest='uz').text, callback_data=f"answer_{question_number}_{option}")]
            for option in options
        ]
    )
    translated_question = translator.translate(question, dest='uz').text
    return await message.answer(translated_question, reply_markup=keyboard)


@dp.callback_query(F.data.startswith('answer_'))
async def handle_answer(call: types.CallbackQuery, state: FSMContext):
    _, question_number, user_answer = call.data.split('_')
    question_number = int(question_number)

    user_data = await state.get_data()
    questions = user_data.get('questions', [])

    if question_number <= len(questions):
        question = questions[question_number - 1]
        correct_answer = question['correct_answer']

        if user_answer == correct_answer:
            await call.message.answer("To'g'ri javob! ✅")
            await state.update_data(correct_answers_count=user_data.get('correct_answers_count', 0) + 1)
        else:
            if is_premium:
                await call.message.answer(f"❌ Xato javob!\nTo'g'ri javob: {translator.translate(correct_answer, dest='uz').text}")
            else:
                await call.message.answer("❌ Xato javob!\nTo'g'ri javobni bilish uchun premiumga obuna bo'lishingiz kerak.")

        previous_message_id = user_data.get('current_message_id')
        if previous_message_id:
            try:
                await call.message.bot.delete_message(call.message.chat.id, previous_message_id)
            except Exception as e:
                logging.error(f"Failed to delete message {previous_message_id}: {e}")

        await state.update_data(current_question_index=question_number)
        await display_question(call.message, state)
    else:
        await call.message.answer("Savollar topilmadi. Iltimos, qaytadan urinib ko'ring.")


@dp.message(Start.quiz_category)
async def handle_invalid_message(message: types.Message):
    await message.answer("Iltimos, to'g'ri tanlov qiling.")



# Premium

@dp.message(Command("premium"))
async def cmd_premium(message: types.Message):
    if is_premium:
        await message.answer("Siz allaqachon premiumga obuna bo'lgansiz 👍")
    else:
        text = (
            "📈 Premium Tarifi Xususiyatlari:\n\n"
            "1. Ko'proq savollar - 30 ta savol olishingiz mumkin!\n"
            "2. Uzoqroq vaqt - Har bir savol uchun 30 daqiqa!\n"
            "3. Eksklyuziv mavzular - Faqat Premium foydalanuvchilar uchun!"
        )
        premium_image_url = "https://www.ixbt.com/img/n1/news/2022/5/2/1_25_large.png"

        await message.answer_photo(photo=premium_image_url, caption=text, reply_markup=buy_premium_button)


@dp.callback_query(F.data == 'buy_premium')
async def handle_buy_premium(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Iltimos, telefon raqamingizni yuboring", reply_markup=share_phone)
    await state.set_state(Premium.phone_number)


class ContactFilter(Filter):
    def __init__(self):
        super().__init__()

    async def __call__(self, message: types.Message) -> bool:
        return message.contact is not None


@dp.message(ContactFilter())
async def handle_phone_number(message: types.Message, state: FSMContext):
    global telegram_id
    phone_number = message.contact.phone_number

    update_phone_number(telegram_id, phone_number)

    await message.answer(
        "To'lov uchun pastdagi tugmani bosing.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="To'lov qilish",
                                  url="https://paypal.com")]
        ])
    )

    await state.clear()

# admin commands
@dp.callback_query(F.data == 'bot_users')
async def handle_users(call: types.CallbackQuery):
    users = readSqliteTable() 
    await call.message.answer(f"Bot foydalanuvchilari: {len(users)} ta", reply_markup=create_show_users_button())

@dp.callback_query(F.data == 'show_bot_users')
async def show_all_users(call: types.CallbackQuery):
    users = readSqliteTable()
    for user in users:
        telegram_id, username, phone_number, is_premium = user
        is_premium_text = 'True' if is_premium == 1 else 'False' 
        user_info = (
            f"Telegram ID: {telegram_id}\n"
            f"Username: @{username}\n"
            f"Telefon raqam: {phone_number}\n"
            f"Premium: {is_premium_text}"
        )
        
        await call.message.answer(user_info, reply_markup=create_premium_toggle_button(telegram_id, is_premium))

@dp.callback_query(lambda c: c.data and c.data.startswith('make_premium'))
async def make_user_premium(call: types.CallbackQuery):
    user_id = int(call.data.split(":")[1])  
    upgrade_user_to_premium(user_id) 
    await call.answer("Foydalanuvchi premiumga a'zo qilindi!", show_alert=True)

@dp.callback_query(lambda c: c.data and c.data.startswith('unmake_premium'))
async def unmake_user_premium(call: types.CallbackQuery):
    user_id = int(call.data.split(":")[1])  
    downgrade_user_from_premium(user_id) 
    await call.answer("Foydalanuvchi premiumdan olib tashlandi!", show_alert=True)

@dp.callback_query(F.data == 'premium_users')
async def handle_premium_users(call: types.CallbackQuery):
    premium_users = readSqliteTable(premium=True)
    if premium_users:
        await call.message.answer(f"Premium foydalanuvchilari soni: {len(premium_users)}", reply_markup=premium_button)
    else:
        await call.message.answer("Hozircha premium foydalanuvchilari yo'q")

@dp.callback_query(F.data == 'get_premium_users')
async def handle_get_premium_users(call: types.CallbackQuery):
    premium_users = readSqliteTable(premium=True)
    for user in premium_users:
        telegram_id, username, phone_number, is_premium = user
        is_premium_text = 'True' if is_premium == 1 else 'False' 
        user_info = (
            f"User ID: {telegram_id}\n"
            f"Username: @{username}\n"
            f"Phone Number: {phone_number}\n"
            f"Premium: {is_premium_text}"
        )
        await call.message.answer(user_info, reply_markup=create_premium_toggle_button(telegram_id, is_premium))

@dp.callback_query(F.data == 'admins')
async def show_admins_button_handler(call: types.CallbackQuery):
    global telegram_id
    if telegram_id == MAIN_ADMIN:
        admins = fetchAllAdmins()
        ADMINS.clear()  
        for admin in admins:
            ADMINS.append(admin[0])
        await call.message.answer(f'Adminlar soni: {len(ADMINS)}', reply_markup=show_admins_button)
    else:
        await call.message.answer("Uzr, siz admin qo'sha yoki o'chira olmaysiz.")

@dp.callback_query(F.data == 'show_admins')
async def show_admins_handler(call: types.CallbackQuery):
    admins = fetchAllAdmins()  # Fetch all admins from the database
    if not admins:
        # No admins found, show the "Admin qo'shish" button
        await call.message.answer(
            "Adminlar yo'q. Iltimos, yangi admin qo'shish uchun quyidagi tugmani bosing.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Admin qo'shish",
                            callback_data="add_admin"
                        )
                    ]
                ]
            )
        )
    else:
        # Display each admin with delete button
        for admin in admins:
            await call.message.answer(
                f'Admin: {admin[0]}',  # Assuming admin[0] is the telegram_id
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="O'chirish",
                                callback_data=f"delete_admin_{admin[0]}"
                            )
                        ]
                    ]
                )
            )

@dp.callback_query(F.data.startswith('delete_admin_'))
async def delete_admin_handler(call: types.CallbackQuery):
    telegram_id_to_delete = call.data.split('_', 2)[-1]  # Extract telegram_id from callback data
    
    # Delete the admin from the database
    deleteAdmin(telegram_id_to_delete)
    
    # Notify the user and refresh the admin list
    await call.message.answer(f"Admin {telegram_id_to_delete} muvaffaqiyatli o'chirildi!", show_alert=True)
    
    # Refresh the list of admins
    await show_admins_handler(call)

@dp.callback_query(F.data == 'add_admin')
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Yangi adminning telegram **id** sini kiriting.')
    await state.set_state(Admin.smth)

@dp.message(Admin.smth)
async def add_admin(message: types.Message, state: FSMContext):
    new_admin_tg_id = message.text
    addAdmin(new_admin_tg_id)
    await message.answer("Yangi admin muvaffaqiyatli qo'shildi!", show_alert=True)
    await state.clear()



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())