from datetime import date
from datetime import datetime
from database.models import User, History
from loguru import logger

from keyboards.inline.city_keyboard import city_markup
from keyboards.inline.run_calendar import run_calendar
from loader import bot
import json
from telebot.types import Message, CallbackQuery, InputMediaPhoto
from states.person_info import PersonInfoState
from utils.city_founding import city_found
from utils.hotel_detail import hotel_detail
from utils.hotels_bestdeal import hotel_bestdeal
from utils.hotels_founding import hotel_found


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def low_price(message: Message) -> None:
    user, __ = User.get_or_create(external_id=message.from_user.id, chat_id=message.chat.id,
                                  name=message.from_user.full_name)
    bot.set_state(message.from_user.id, PersonInfoState.input_city, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username} введите город')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data.clear()
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

        count_age = int(data['children_count'])
        if count_age == 0:
            bot.set_state(message.from_user.id, PersonInfoState.hotels_quantity, message.chat.id)
            bot.send_message(message.from_user.id, 'Введите кол-во выводимых отелей:')

        elif count_age == 1:
            text_count = 'вашего ребенка'
            bot.set_state(message.from_user.id, PersonInfoState.children_age, message.chat.id)
            bot.send_message(message.from_user.id, f'Введите возвраст {count_age} {text_count}:')
        else:
            text_count = 'ваших детей'
            bot.set_state(message.from_user.id, PersonInfoState.children_age, message.chat.id)
            bot.send_message(message.from_user.id, f'Введите возраст {count_age} {text_count} через пробел:')
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом больше или равно 0')


@bot.message_handler(state=PersonInfoState.children_age)
def children_age(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        age = message.text.split()
        data['children'] = []
        for i_age in age:
            data['children'].append({'age': int(i_age)})

    run_calendar(message, id=1)

    # bot.set_state(message.from_user.id, PersonInfoState.hotels_quantity, message.chat.id)
    # bot.send_message(message.from_user.id, 'Введите кол-во выводимых отелей (не больше 25):')


@bot.message_handler(state=PersonInfoState.hotels_quantity)
def hotels_count(message: Message):
    if message.text.isdigit() and int(message.text) <= 25:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotel_count'] = int(message.text)
        if data['command'] == '/bestdeal':
            bot.set_state(message.from_user.id, PersonInfoState.min_price, message.chat.id)
            bot.send_message(message.from_user.id, 'Введите минимальную стоимость')
        else:
            bot.set_state(message.from_user.id, PersonInfoState.photo_quantity, message.chat.id)
            bot.send_message(message.from_user.id, 'Введите кол-во выводимых фото (не больше 10) или 0, если фото не нужны')
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом больше и не больше 25')


@bot.message_handler(state=PersonInfoState.min_price)
def minimal_price(message: Message):
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price'] = int(message.text)
        bot.set_state(message.from_user.id, PersonInfoState.max_price, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите максимальную стоимость')


@bot.message_handler(state=PersonInfoState.max_price)
def maximum_price(message: Message):
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_price'] = int(message.text)
        bot.set_state(message.from_user.id, PersonInfoState.start_range, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите начало диапозона расстояния от центра, если дробное число через точку(в км)')


@bot.message_handler(state=PersonInfoState.start_range)
def start_range(message: Message):
    if message.text.isdigit() or is_number(message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['start_range'] = float(message.text) * 0.62137
        bot.set_state(message.from_user.id, PersonInfoState.end_range, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите конец диапозона расстояния от центра, если дробное число через точку(в км)')


@bot.message_handler(state=PersonInfoState.end_range)
def end_range(message: Message):
    if message.text.isdigit() or is_number(message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['end_range'] = float(message.text) * 0.62137
        bot.set_state(message.from_user.id, PersonInfoState.photo_quantity, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите кол-во выводимых фото (не больше 10) или 0, если фото не нужны')


@bot.message_handler(state=PersonInfoState.photo_quantity)
def photo_count(message: Message):
    flag = True
    if message.text.isdigit() and int(message.text) <= 10:
        user, __ = User.get_or_create(external_id=message.from_user.id, chat_id=message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_count'] = int(message.text)
            count_days = abs(data['departure'] - data['arrival'])
        if data['command'] == '/highprice' or data['command'] == '/lowprice':
            hotel = hotel_found(data)
        elif data['command'] == '/bestdeal':
            hotel = hotel_bestdeal(data)
        if hotel.status_code == 200:
            hotels = hotel.json()
            if 'errors' in hotels:
                bot.send_message(message.from_user.id, 'Отелей с такими параметрами не найдено')
                flag = True
            else:
                if data['command'] == '/bestdeal':
                    count = 0
                    for i_elem in hotels['data']['propertySearch']["properties"]:
                        if (data['start_range'] < i_elem['destinationInfo']['distanceFromDestination']['value'] <
                                data['end_range']):
                            name_hotel = i_elem['name']
                            id_hotel = i_elem['id']
                            period = i_elem['price']['priceMessages'][1]['value']
                            logger.info(period)
                            score = i_elem['reviews']['score']
                            price = round(i_elem['price']['lead']['amount'], 1)
                            total_price = round(price * count_days.days, 1)
                            center_info = round(float(i_elem['destinationInfo']['distanceFromDestination']['value']) / 0.62137, 1)

                            text = f'Название отеля: {name_hotel}\nРейтинг отеля: {score}\nПериод: {period}\n' \
                                   f'Расстояние от центра(в км): {center_info}\nЦена за ночь: {price}\n' \
                                   f'Всего за период: {total_price}\nСсылка на отель:\n' \
                                   f'https://www.hotels.com/h{id_hotel}.Hotel-Information'
                            history = History.create(user_id=user, command=data['command'], message=text)
                            if data['photo_count'] > 0:
                                photos_hotel = hotel_detail(id_hotel, data['photo_count'])
                                media_group = []
                                for num, url in enumerate(photos_hotel):
                                    media_group.append(InputMediaPhoto(media=url, caption=text if num == 0 else ''))

                                bot.send_media_group(message.from_user.id, media=media_group)
                            else:
                                bot.send_message(message.chat.id, text)
                            flag = True
                            count += 1
                            if count == data['hotel_count']:
                                break
                elif data['command'] == '/lowprice':
                    for i_elem in hotels['data']['propertySearch']["properties"][:data['hotel_count']]:
                        name_hotel = i_elem['name']
                        id_hotel = i_elem['id']
                        period = i_elem['price']['priceMessages'][1]['value']
                        logger.info(period)
                        score = i_elem['reviews']['score']
                        price = round(i_elem['price']['lead']['amount'], 1)
                        total_price = round(price * count_days.days, 1)

                        text = f'Название отеля: {name_hotel}\nРейтинг отеля: {score}\nПериод: {period}\n' \
                               f'Цена за ночь: {price}\n' \
                               f'Всего за период: {total_price}\nСсылка на отель:\n' \
                               f'https://www.hotels.com/h{id_hotel}.Hotel-Information'
                        history = History.create(user_id=user, command=data['command'], message=text)
                        if data['photo_count'] > 0:
                            photos_hotel = hotel_detail(id_hotel, data['photo_count'])
                            media_group = []
                            for num, url in enumerate(photos_hotel):
                                media_group.append(InputMediaPhoto(media=url, caption=text if num == 0 else ''))

                            bot.send_media_group(message.from_user.id, media=media_group)
                        else:
                            bot.send_message(message.chat.id, text)
                        flag = True
                elif data['command'] == '/highprice':
                    tmp_price = []
                    tmp_hotel = []
                    for i_elem in hotels['data']['propertySearch']["properties"]:
                        tmp_hotel.append(i_elem)
                        price_ = i_elem['price']['lead']['amount']
                        tmp_price.append(price_)
                    price_hotel = sorted(tmp_price, reverse=True)
                    hotel_count = 0
                    for price in price_hotel:
                        if hotel_count == data['hotel_count']:
                            break
                        for i_elem in tmp_hotel:
                            if price == i_elem['price']['lead']['amount']:
                                name_hotel = i_elem['name']
                                id_hotel = i_elem['id']
                                period = i_elem['price']['priceMessages'][1]['value']
                                logger.info(period)
                                score = i_elem['reviews']['score']
                                total_price = round(price * count_days.days, 1)

                                text = f'Название отеля: {name_hotel}\nРейтинг отеля: {score}\nПериод: {period}\n' \
                                       f'Цена за ночь: {price}\n' \
                                       f'Всего за период: {total_price}\nСсылка на отель:\n' \
                                       f'https://www.hotels.com/h{id_hotel}.Hotel-Information'
                                history = History.create(user_id=user, command=data['command'], message=text)
                                if data['photo_count'] > 0:
                                    photos_hotel = hotel_detail(id_hotel, data['photo_count'])
                                    media_group = []
                                    for num, url in enumerate(photos_hotel):
                                        media_group.append(InputMediaPhoto(media=url, caption=text if num == 0 else ''))

                                    bot.send_media_group(message.from_user.id, media=media_group)
                                else:
                                    bot.send_message(message.chat.id, text)
                                flag = True
                                hotel_count += 1

        else:
            bot.send_message(message.from_user.id, 'Отелей с такими параметрами не найдено')
            flag = True

    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом меньше или равно 10')
        flag = False

    if flag:
        bot.delete_state(message.from_user.id, message.chat.id)


def is_number(stroka: str):
    try:
        float(stroka)
        return True
    except ValueError:
        return False