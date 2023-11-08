from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from database import models

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
