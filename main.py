import telebot
import random
from telebot.types import Message
import time, threading
import schedule
from telebot import TeleBot


bot = telebot.TeleBot("")


@bot.message_handler(commands=["start"])
def start_cmd(message: Message):
    bot.send_message(message.chat.id, "Привет! Я тестовый бот. Нажми /about чтобы узнать больше информации о боте ")


@bot.message_handler(commands=["coin"])
def coin_cmd(message: Message):
    x = random.randint(0,1)
    if x == 0:
        bot.reply_to(message.chat.id, "Вам выпал орел!")
    else:
        bot.reply_to(message.chat.id, "Вам выпала решка!")


@bot.message_handler(commands=["about"])
def about_cmd(message: Message):
    text = '<u><b>Мои команды:</b></u>\n/start - <i> запускает бота </i> \n/about - <i> О боте </i> \n/coin - <i>Орел и решка</i>\n/knb - <i>камень/ножницы/бумага</i>\n/timer - <i>таймер</i>\n'
    bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(commands=["knb"])
def knb_cmd(message: Message):
    bot.send_message(message.chat.id, 'Игра запустилась, напишите камень/ножницы/бумага или отмена(чтобы отменить игру) ')
    bot.register_next_step_handler(message, knb_game)

def knb_game(message: Message):
    text = message.text.lower()
    if text == 'отмена':
        bot.send_message(message.chat.id, 'Игра остановлена, вам снова доступны все команды')
        return
    if text not in ['камень','ножницы','бумага']:
        bot.send_message(message.chat.id, "ы написали что то не то, игра остановлена, вам снова доступны все команды")
        return
    comp= random.choice(['камень','ножницы','бумага'])
    if text == comp:
        bot.send_message(message.chat.id, 'Ничья, если хотите поиграть снова, пишите /knb')
        return
    elif (text == 'камень' and bot == 'ножницы') or (text == 'ножницы' and bot == 'бумага') or (text == 'бумага' and bot == 'камень'):
        bot.send_message(message.chat.id, "Вы победили, если хотите поиграть снова, напишите /knb")
        return
    else:
        bot.send_message(message.chat.id, "Вы проиграли, если хотите поиграть снова, напишите /knb")
        return
    

@bot.message_handler(commands=['timer'])
def send_welcome(message):
    bot.reply_to(message, "Используй /set <секунды>  чтобы установить таймер")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Бииип!')


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        bot.reply_to(message, f'Таймер установлен на {sec} секунд.')
        threading.Timer(sec, beep, args=[message.chat.id]).start()
    else:
        bot.reply_to(message, 'Используй так: /set <секунды>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)


bot.infinity_polling()
