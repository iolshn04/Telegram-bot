from telebot.types import Message

from loader import bot


@bot.message_handler(func=lambda message: message.text.lower() == 'привет')
@bot.message_handler(func=lambda message: message.text == '/hello-world')
@bot.message_handler(commands=["hello_world"])
def bot_welcome(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
