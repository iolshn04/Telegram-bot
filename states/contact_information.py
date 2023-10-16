from telebot.handler_backends import State, StatesGroup


class UserInfoStates(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    phone_number = State()