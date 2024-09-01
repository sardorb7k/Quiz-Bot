from aiogram.fsm.state import State, StatesGroup

class Start(StatesGroup):
    quiz_category = State()  
    num_questions = State()      
    difficulty = State()
    type = State()

class Premium(StatesGroup):
    phone_number = State()

class Admin(StatesGroup):
    smth = State()