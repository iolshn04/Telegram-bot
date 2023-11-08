from loader import bot
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date

from states.person_info import PersonInfoState

count = 1
LSTEP_RU = {'y': 'год', 'm': 'месяц', 'd': 'день'}


def run_calendar(message, id):
    if id == 1:
        text = 'заезда'
    elif id == 2:
        text = 'выезда'
    calendar, step = DetailedTelegramCalendar(min_date=date.today(), locale='ru').build()
    bot.send_message(message.chat.id,
                     f"Выберите дату {text} {LSTEP_RU[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar(min_date=date.today(), locale='ru').process(c.data)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP_RU[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        global count
        if count == 1:
            with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
                data['check_in_date'] = {'day': result.day, 'month': result.month, 'year': result.year}
                data['arrival'] = result
            run_calendar(c.message, 2)
            count += 1
        elif count == 2:
            with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
                data['check_out_date'] = {'day': result.day, 'month': result.month, 'year': result.year}
                data['departure'] = result
                bot.set_state(c.from_user.id, PersonInfoState.hotels_quantity, c.message.chat.id)
                bot.send_message(c.from_user.id, 'Введите кол-во выводимых отелей (не больше 25):')
            count = 1





