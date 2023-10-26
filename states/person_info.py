from telebot.handler_backends import State, StatesGroup


class PersonInfoState(StatesGroup):
    input_city = State()
    destination_id = State()
    adults_quantity = State()
    children_quantity = State()
    children_age = State()
    hotels_quantity = State()
    min_price = State()
    max_price = State()
    start_range = State()
    end_range = State()
    photo_quantity = State()
