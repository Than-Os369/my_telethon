import telebot
import time

bot_token = 'sorry but can\'t share the token'
bot = telebot.TeleBot(token=bot_token)

def find_at(msg):
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')

@bot.message_handler(command=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Send it a username')

@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
def at_answer(message):
    texts = message.text.split()
    at_text = find_at(texts)
    if at_text == '@': # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)

while True:
    try:
        bot.polling()

    except Exception:
        time.sleep(15)
