import telebot
import setu
import time
import os

if os.path.exists("token.txt"):
    with open("token.txt", "r") as f:
        TOKEN = f.read()
else:
    print("请在本文件目录下创建token.txt文件，并将token写入其中")
    exit()

bot = telebot.TeleBot(TOKEN)
print("\n=============Start============")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "欢迎来到色图bot！")
    bot.send_message(message.chat.id, "请发送 /setu")


@bot.message_handler(commands=['setu'])
def send_setu(message):
    r18 = 2  # 1:r18，2:全部
    if 'r18' in message.text:
        r18 = 1
    bot.reply_to(message, "正在获取色图...")
    print(time.time(), "，chat_id：", message.chat.id, "，开始获取色图...")
    data = setu.fetch_setu(r18)
    photo = data.get('data')[0].get('urls').get('original')
    try:
        bot.send_photo(message.chat.id, photo)
        if r18 == 1:
            bot.send_message(message.chat.id, "你选择了只发送r18色图，如果想要发送全部色图，请使用 /setu")
        else:
            bot.send_message(message.chat.id, "你选择了发送全部色图，如果想要只发送r18色图，请使用 /setu r18")
    except Exception as e:
        print(e)
        bot.reply_to(message, "获取失败，请稍后再试！")
        print(time.time(), "，chat_id：", message.chat.id, "，获取失败！")


bot.polling()
