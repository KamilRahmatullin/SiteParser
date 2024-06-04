from aiogram import Bot

from config import env

# конфиг для бота
bot = Bot(env('TOKEN_API'))