# -*- coding: UTF-8 -*-
import telebot
import setu
import time
import os
import pixiv
import html2text
from pprint import pprint


def main():
    global bot
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
        photo = data['data'][0]['urls']['original']
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

    @bot.message_handler(commands=['pixiv'])
    def send_pixiv(message):
        # 提取请求参数
        num = 10  # 默认10条
        #r18 = False # 默认不发送r18
        if 'num=' in message.text:
            num = int(message.text.split('num=')[1])
        #if 'r18' in message.text:
            #r18 = True

        bot.reply_to(message, "正在获取pixiv...")
        print(time.time(), "，chat_id：", message.chat.id, "，开始获取pixiv...")
        try:
            api = pixiv.pixiv_login()
            bot.send_message(message.chat.id, "正在获取pixiv排行榜...")
            #if r18:
                #mode = "daily_r18"
                #bot.send_message(message.chat.id, "你选择了r18模式！")
            #else:
                #mode = "day"
            for now_item in range(0, num):
                # item_cover_img 存储的是图片的url
                # item_pixiv_id 存储的是插画的id

                (item_cover_img, item_pixiv_id) = (
                    pixiv.deal_ranking(pixiv.get_ranking(api), now_item),
                    pixiv.get_ranking(api)['illusts'][now_item]['id'])

                bot.send_message(message.chat.id, "正在发送pixiv排行榜第" + str(now_item + 1) + "张...")
                button = telebot.types.InlineKeyboardButton(text="查看详情", callback_data="pixiv_" + str(item_pixiv_id))

                message_sent = bot.send_photo(message.chat.id, pixiv.download_illust(item_cover_img),
                                              reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))

        except Exception as e:
            print(e)
            bot.reply_to(message, "获取失败，请稍后再试！")
            print(time.time(), "，chat_id：", message.chat.id, "，获取失败！")

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        bot.send_message(call.message.chat.id, "正在获取详情...")

        if call.data.startswith("pixiv_"):
            pixiv_id = call.data.split("_")[1]
            api = pixiv.pixiv_login()
            detail = pixiv.get_pixiv_detail(api, pixiv_id)

            # 获取各种信息
            caption_not_empty = False
            if detail['illust']['caption'] != "":  # 检查插画有caption
                caption = detail['illust']['caption']  # 插画caption，HTML格式
                caption = html2text.html2text(caption)  # 转换为Markdown格式
                caption_not_empty = True
            title = detail['illust']['title']
            creat_date = detail['illust']['create_date']  # 插画创建时间
            meta_pages = detail['illust']['meta_pages']  # 插画的所有页面，一个列表

            # 发送消息
            if caption_not_empty:
                bot.send_message(call.message.chat.id, caption, parse_mode="Markdown")
            bot.send_message(call.message.chat.id,
                             "标题：" + title + "\n" + "创建时间：" + creat_date + "\n" + "页数：" + str(
                                 len(meta_pages)) + "（若页数为零则插画为单页）")
            for i in range(0, len(meta_pages)):
                bot.send_document(call.message.chat.id, pixiv.download_illust(meta_pages[i]['image_urls']['original']),
                                  caption=title + " 第" + str(i + 1) + "页")
            bot.send_message(call.message.chat.id, "完成！")
            print(time.time(), "，chat_id：", call.message.chat.id, "，获取详情完成！")

    bot.polling()
