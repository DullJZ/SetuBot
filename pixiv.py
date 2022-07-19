from pixivpy3 import *
import os
import html2text
import requests
import json
from pprint import *

# 初始化pixiv REFRESH_TOKEN
if os.path.exists("pixiv_token.txt"):
    with open("pixiv_token.txt", "r") as f:
        REFRESH_TOKEN = f.read()
else:
    print("请在本文件目录下创建pixiv_token.txt文件，并将refresh_token写入其中")
    exit()


def pixiv_login():
    """
    登录pixiv
    返回pixivapi对象
    """
    api = AppPixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)
    return api


def deal_ranking(ranking, now_item=0):
    """
    处理排行榜
    ranking: 排行榜json数据
    now_item: 当前项目
    """
    item = ranking['illusts'][now_item]
    print(item['id'], item['title'], item['image_urls']['large'])
    return item['image_urls']['large']


def download_illust(url):
    """
    下载图片
    返回图片内容bytes
    """
    print("开始下载：", url)
    img = requests.get(url, stream=True, headers={'Referer': 'https://app-api.pixiv.net/'})
    return img.content


def get_pixiv_detail(api, illust_id):
    """
    通过插画id获取详情
    返回详情json数据
    """
    pixiv_detail = api.illust_detail(illust_id)
    return pixiv_detail


def handle_pixiv_detail(detail):
    """
    处理插画详情
    传入详情json数据
    返回一个元组 (p:消息内容, caption ,caption_not_empty:是否有描述, original_image_urls:包含图片url的一个列表)
    """
    # 获取各种信息
    id = detail['illust']['id']
    caption = None
    caption_not_empty = False
    if detail['illust']['caption'] != "":  # 检查插画有caption
        caption = detail['illust']['caption']  # 插画caption，HTML格式
        caption = html2text.html2text(caption)  # 转换为Markdown格式
        caption_not_empty = True

    title = detail['illust']['title']
    creat_date = detail['illust']['create_date']  # 插画创建时间
    meta_pages = detail['illust']['meta_pages']  # 插画的所有页面，一个列表

    # 消息内容
    p = "插画ID：{0}\n标题：{1}\n创建时间：{2}\n页数：{3}".format(id, title, creat_date, str(
        len(meta_pages)) + "（若页数为零则插画为单页）")

    # original_image_urls为返回的包含源图片url的一个列表
    original_image_urls = []
    if not meta_pages:
        original_image_urls = [detail['illust']['meta_single_page']['original_image_url']]
    else:
        for i in range(0, len(meta_pages)):
            original_image_urls.append(meta_pages[i]['image_urls']['original'])
    return p, caption, caption_not_empty, original_image_urls


def handle_search_illust(search_data):
    """
    处理搜索结果
    传入搜索结果json数据
    返回一个列表IDs，包含插画id
    """
    IDs = []
    for i in search_data['illusts']:
        IDs.append(i['id'])
    return IDs
