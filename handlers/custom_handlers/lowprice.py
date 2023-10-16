from keyboards.inline.city_keyboard import city_markup
from loader import bot
from telebot.types import Message, CallbackQuery
from states.person_info import PersonInfoState
from utils.city_founding import city_found
from utils.hotels_founding import hotel_found


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message) -> None:
    bot.set_state(message.from_user.id, PersonInfoState.input_city, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username} введите город')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text


@bot.message_handler(state=PersonInfoState.input_city)
def get_city(message: Message) -> None:
    cities = city_found(message.text)
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_markup(cities))

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.callback_query_handler(func=lambda callback: callback.data)
def city_choice(callback: CallbackQuery):
    if callback.message:
        bot.set_state(callback.from_user.id, PersonInfoState.destination_id, callback.message.chat.id)
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['destination_id'] = callback.data
        bot.set_state(callback.from_user.id, PersonInfoState.adults_quantity, callback.message.chat.id)
        bot.send_message(callback.from_user.id, "Введите кол-во взрослых:")


@bot.message_handler(state=PersonInfoState.adults_quantity)
def adult_count(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, PersonInfoState.children_quantity, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите кол-во детей: ')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['adults'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Количетсво может быть только числом больше 0')


@bot.message_handler(state=PersonInfoState.children_quantity)
def children_count(message: Message):
    if message.text.isdigit() and int(message.text) >= 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children_count'] = message.text

            # for i in range(int(data['children_count'])):
            #     bot.send_message(message.from_user.id, f'Введите возраст {i}-го ребенка: ')
            #     data['children'] = [{'age': message.text}]
        count_age = int(data['children_count'])
        if count_age == 0:
            bot.set_state(message.from_user.id, PersonInfoState.hotels_quantity, message.chat.id)
            bot.send_message(message.from_user.id, 'Введите кол-во выводимых отелей:')

        elif count_age == 1:
            text_count = 'вашего ребенка'
            bot.set_state(message.from_user.id, PersonInfoState.children_age, message.chat.id)
            bot.send_message(message.from_user.id, f'Введите возвраст {count_age} {text_count} через пробел:')
        else:
            text_count = 'ваших детей'
            bot.set_state(message.from_user.id, PersonInfoState.children_age, message.chat.id)
            bot.send_message(message.from_user.id, f'Введите возвраст {count_age} {text_count} через пробел:')
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом больше или равно 0')


@bot.message_handler(state=PersonInfoState.children_age)
def children_age(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        age = message.text.split()
        data['children'] = []
        for i_age in age:
            data['children'].append({'age': int(i_age)})

    bot.set_state(message.from_user.id, PersonInfoState.hotels_quantity, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите кол-во выводимых отелей (не больше 25):')


@bot.message_handler(state=PersonInfoState.hotels_quantity)
def hotels_count(message: Message):
    if message.text.isdigit() and int(message.text) <= 25:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotel_count'] = int(message.text)

        bot.set_state(message.from_user.id, PersonInfoState.photo_quantity, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите кол-во выводимых фото (не больше 10):')
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом больше и не больше 25')


@bot.message_handler(state=PersonInfoState.photo_quantity)
def photo_count(message: Message):
    if message.text.isdigit() and int(message.text) <= 10:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_count'] = int(message.text)

        bot.set_state(message.from_user.id, PersonInfoState.check_in_date, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите дату заезда через точку DD.MM.YYYY')
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом меньше или равно 10')


@bot.message_handler(state=PersonInfoState.check_in_date)
def check_in(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        date = message.text.split('.')
        data['check_in_date'] = {'day': int(date[0]), 'month': int(date[1]), 'year': int(date[2])}

    bot.set_state(message.from_user.id, PersonInfoState.check_out_date, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите дату выезда через точку DD.MM.YYYY')


@bot.message_handler(state=PersonInfoState.check_out_date)
def check_out(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        date = message.text.split('.')
        data['check_out_date'] = {'day': int(date[0]), 'month': int(date[1]), 'year': int(date[2])}
    hotels = hotel_found(data)
    print(hotels)
