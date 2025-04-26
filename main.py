import telebot
import random
from telebot.types import Message



bot = telebot.TeleBot("7606191233:AAHijb2uiEMQfBTTfGTFPc_z2Fg28n6HcWg")


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
    




bot.infinity_polling()
