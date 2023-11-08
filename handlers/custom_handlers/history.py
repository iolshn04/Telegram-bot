from telebot.types import Message
from database.models import User, History
from loader import bot


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    user = User.select().where(User.external_id == message.from_user.id).get()
    history = History.select().where(History.user_id == user).limit(10).order_by(History.id.desc())
    for hist in history.execute():
        bot.send_message(message.from_user.id, f'Команда: {hist.command}\nОтель: {hist.message} ')