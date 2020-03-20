!pip install pyTelegramBotAPI

import telebot
import time
import requests

def utube(the_link, num_search=3):
    utube_content = requests.get(the_link)
    parent_index = utube_content.text.find('<h3 class="yt-lockup-title ">') + len('<h3 class="yt-lockup-title ">')
    links = []
    for i in range(42):
        child1 = utube_content.text[parent_index:].find('href="') + len('href="')
        child2 = utube_content.text[(parent_index + child1):].find('" cl')
        final_link = utube_content.text[(parent_index + child1):(parent_index + child1 + child2)]
        links.append(final_link)
        parent_index += child1 + child2 + len('" cl')

    links = [i for i in links if '/watch' in i]
    links = [i for i in links if len(i) < 42]
    flinks = []
    for i in range(len(links)):
        if links[i] not in flinks:
            flinks.append(links[i])
    if len(flinks) > num_search:
        return flinks[:num_search]
    else:
        return flinks

def calculator(the_operands):
  print(the_operands[2])
  the_ops = the_operands
  nums = (float(the_ops[1]), float(the_ops[-1]))
  a, b = nums
  # comp_dict = {
  #     '*': (a*b),
  #     '+': (a+b),
  #     '/': (a/b),
  #     '-': (a-b),
  #     '**': (a**int(b)),
  #     '%': (a%int(b))
  # }

  if the_ops[2] == "*":
    return a * b
  if the_ops[2] == "+":
    return a + b
  if the_ops[2] == "/":
    return a/b
  if the_ops[2] == "-":
    return a - b
  if the_ops[2] == "**":
    return a ** b
  if the_ops[2] == "%":
    return a % b

def dictionary(the_word):
    the_web = "https://dictionary.cambridge.org/dictionary/english/" + the_word
    connects = requests.get(the_web)
    content = connects.text.find('content="'+the_word+' definition:') + len('content="'+the_word+' definition:')
    if content != -1+len('content="'+the_word+' definition:'):
        mgs = ['3.', '&']
        for i in mgs:
          if connects.text[content:content+666].find(i) != -1:
            meaning = connects.text[content:].find(i)
            break
        return connects.text[content:(meaning+content)]
    else:
        return "Unknown word, HUMAN"

bot_token = 'sorry but this is private'
bot = telebot.TeleBot(token=bot_token)

def find_at(msg):
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = "Hello user, I am a simple bot created by @null_z and enjoy"
    bot.reply_to(message, msg)

@bot.message_handler(command=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Send it a username')

@bot.message_handler(func=lambda msg: msg.text is not None)
def at_answer(message):
    texts = message.text.split()
    if texts[0].lower() == 'yt':
      linking = "https://www.youtube.com/results?search_query={}".format('+'.join(texts[:len(texts)-2]))
      if texts[-1].isdigit():
        if int(texts[-1]) > 0:
          the_links = utube(linking, int(texts[-1]))
          if the_links:
              for i in range(len(the_links)):
                  utube_link = "https://www.youtube.com{}".format(the_links[i])
                  bot.reply_to(message, utube_link)
        if int(texts[-1]) == 0:
          bot.reply_to(message, "If u want 0 videos then doesn't that defeat the purpose of searching for it in the first place, SIR/MA'AM!")
      else:
        the_links = utube(linking)
        for i in range(len(the_links)):
          utube_link = "https://www.youtube.com{}".format(the_links[i])
          bot.reply_to(message, utube_link)

    if texts[0].lower() == 'calc':
      ans = calculator(texts)
      bot.reply_to(message, ans)

    if texts[0].lower() == 'dict':
      meaning = dictionary(texts[1])
      bot.reply_to(message, meaning)

    # elif texts[0].lower() == 'dict':
    #     the_meaning = dictionary(texts[1])
    #     bot.reply_to(message, the_meaning)

while True:
    try:
        bot.polling()

    except Exception:
        time.sleep(3)
