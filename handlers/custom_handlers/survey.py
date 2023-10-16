from keyboards.reply.contact import request_contact
from loader import bot
from telebot.types import Message
from states.contact_information import UserInfoStates


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoStates.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет {message.from_user.username} введите свое имя')


@bot.message_handler(state=UserInfoStates.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо записал, теперь введите свой возраст')
        bot.set_state(message.from_user.id, UserInfoStates.age, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Имя может содержать только буквы')


@bot.message_handler(state=UserInfoStates.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал, теперь введите страну проживания')
        bot.set_state(message.from_user.id, UserInfoStates.country, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Возраст может быть только числом')


@bot.message_handler(state=UserInfoStates.country)
def get_country(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо записал, теперь введите свой город')
    bot.set_state(message.from_user.id, UserInfoStates.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text


@bot.message_handler(state=UserInfoStates.city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     'Спасибо записал, отправьте свой номер, нажав на кнопку',
                     reply_markup=request_contact()
                     )
    bot.set_state(message.from_user.id, UserInfoStates.phone_number, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(content_types=['text', 'contact'], state=UserInfoStates.phone_number)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number

            text = f'Спасибо за предоставленную вами информацию ваши данные: \n' \
                   f'Имя - {data["name"]}\nВозраст - {data["age"]}\nСтрана - {data["country"]}\n' \
                   f'Город - {data["city"]}\nНомер телефона - {data["phone_number"]}'
            bot.send_message(message.from_user.id, text)
            flag = True

    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить контактную информацию нажмите на кнопку')
        flag = False
    if flag:
        bot.delete_state(message.from_user.id, message.chat.id)