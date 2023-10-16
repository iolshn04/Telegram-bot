from telebot.handler_backends import State, StatesGroup


class PersonInfoState(StatesGroup):
    input_city = State()
    destination_id = State()
    adults_quantity = State()
    children_quantity = State()
    children_age = State()
    hotels_quantity = State()
    photo_quantity = State()
    check_in_date = State()
    check_out_date = State()