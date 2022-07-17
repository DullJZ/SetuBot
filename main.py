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
    def start(message):
        bot.reply_to(message, "欢迎来到色图bot！")
        bot.send_message(message.chat.id, "请发送 /setu")

    @bot.message_handler(commands=['fetch_tg_user_by_id'])
    def fetch_tg_user_by_id(message):
        user_id = message.text.split(" ")[1]
        user = bot.get_chat(user_id)
        if user.type == "private":
            button = telebot.types.InlineKeyboardButton(text="查看用户详情", url='tg://user?id={0}'.format(user_id))
            if user.username:
                bot.send_message(message.chat.id, "@" + user.username,
                                 reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))
            else:
                bot.send_message(message.chat.id, "用户未设置用户名",
                                 reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))
        elif user.type == "group":
            if user.invite_link:
                button = telebot.types.InlineKeyboardButton(text="查看群详情", url=user.invite_link)
                bot.send_message(message.chat.id, "这是一个群组：" + user.title,
                                 reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))
            else:
                bot.send_message(message.chat.id, "群组未设置或无权限访问邀请链接，群组：" + user.title)
        elif user.type == "supergroup":
            bot.send_message(message.chat.id, "@" + user.username)

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

    @bot.message_handler(commands=['pixiv_ranking'])
    def send_pixiv_ranking(message):
        # 提取请求参数
        num = 10  # 默认10条
        r18 = False  # 默认不发送r18
        if 'num=' in message.text:
            num = int(message.text.split('num=')[1])
        if 'r18' in message.text:
            r18 = True

        bot.reply_to(message, "正在获取pixiv...")
        print(time.time(), "，chat_id：", message.chat.id, "，开始获取pixiv...")
        try:
            api = pixiv.pixiv_login()
            bot.send_message(message.chat.id, "正在获取pixiv排行榜...")
            if r18:
                mode = "day_r18"
                bot.send_message(message.chat.id, "你选择了r18模式！")
            else:
                mode = "day"
            for now_item in range(0, num):
                # item_cover_img 存储的是图片的url
                # item_pixiv_id 存储的是插画的id
                item_cover_img = pixiv.deal_ranking(api.illust_ranking(mode), now_item)
                item_pixiv_id = api.illust_ranking(mode)['illusts'][now_item]['id']

                bot.send_message(message.chat.id, "正在发送pixiv排行榜第" + str(now_item + 1) + "张...")
                button = telebot.types.InlineKeyboardButton(text="查看详情", callback_data="pixiv_" + str(item_pixiv_id))

                message_sent = bot.send_photo(message.chat.id, pixiv.download_illust(item_cover_img),
                                              reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))

        except Exception as e:
            print(e)
            bot.reply_to(message, "获取失败，请稍后再试！")
            print(time.time(), "，chat_id：", message.chat.id, "，获取失败！")

    @bot.message_handler(commands=['pixiv_id'])
    def get_detail_by_id(message):

        api = pixiv.pixiv_login()
        detail = pixiv.get_pixiv_detail(api, message.text.split(' ')[1])
        p, caption, caption_not_empty, original_image_urls = pixiv.handle_pixiv_detail(detail)
        # 发送消息
        if caption_not_empty:
            bot.send_message(message.chat.id, caption, parse_mode="Markdown")
        bot.send_message(message.chat.id, p)
        j = 0  # 图片序号
        for i in original_image_urls:
            bot.send_document(message.chat.id, pixiv.download_illust(i),
                              visible_file_name=" 第" + str(j) + "页.png", disable_notification=True)
            j += 1
        bot.send_message(message.chat.id, "完成！")
        print(time.time(), "，chat_id：", message.chat.id, "，获取详情完成！")

    @bot.message_handler(commands=['pixiv_search'])
    def pixiv_search(message):
        word = message.text.split(' ')[1]
        num = 10  # 默认10条
        if 'num=' in message.text:
            num = int(message.text.split('num=')[1])
        api = pixiv.pixiv_login()
        search_data = api.search_illust(word)

        index = 0
        if num > 30:
            num = 30
            bot.send_message(message.chat.id, "搜索结果超过30条，只显示前30条！")

        for id in pixiv.handle_search_illust(search_data):
            # 检测是否超过num
            index += 1
            if index > num:
                break

            detail = pixiv.get_pixiv_detail(api, id)
            # 封面图片
            cover_img = detail['illust']['image_urls']['large']
            # 发送消息
            button = telebot.types.InlineKeyboardButton(text="查看详情", callback_data="pixiv_" + str(id))
            bot.send_photo(message.chat.id, pixiv.download_illust(cover_img),
                           reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        bot.send_message(call.message.chat.id, "正在获取详情...")
        api = pixiv.pixiv_login()

        # 提取插画id
        pixiv_id = call.data.split("_")[1]
        detail = pixiv.get_pixiv_detail(api, pixiv_id)
        p, caption, caption_not_empty, original_image_urls = pixiv.handle_pixiv_detail(detail)

        # 发送消息
        if caption_not_empty:
            bot.send_message(call.message.chat.id, caption, parse_mode="Markdown")
        bot.send_message(call.message.chat.id, p)
        j = 0  # 图片序号
        for i in original_image_urls:
            bot.send_document(call.message.chat.id, pixiv.download_illust(i),
                              visible_file_name=" 第" + str(j) + "页.png", disable_notification=True)
            j += 1
        bot.send_message(call.message.chat.id, "完成！")
        print(time.time(), "，chat_id：", call.message.chat.id, "，获取详情完成！")

    bot.polling()
