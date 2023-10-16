from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Dict


def city_markup(cities: Dict):
    destinations = InlineKeyboardMarkup()
    for id, name in cities.items():
        destinations.add(InlineKeyboardButton(text=name, callback_data=id))

    return destinations
