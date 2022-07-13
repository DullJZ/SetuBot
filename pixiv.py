from pixivpy3 import *
import os
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


def get_illust(api, illust_id):
    illust = api.illust_detail(illust_id)
    print("\n获取到：", illust)
    return illust


def get_ranking(api, mode='day'):
    """
    获取排行榜
    返回排行榜json数据
    mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
    """
    mode = "day"
    ranking = api.illust_ranking(mode=mode)
    return ranking


def deal_ranking(ranking, now_item=0):
    """
    处理排行榜
    ranking: 排行榜json数据
    now_item: 当前项目
    """
    item = ranking.get('illusts')[now_item]
    print(item.get('id'), item.get('title'), item.get('image_urls').get('large'))
    return item.get('image_urls').get('large')


def download_illust(url):
    """
    下载图片
    返回图片内容bytes
    """
    print("\n开始下载：", url)
    img = requests.get(url, stream=True, headers={'Referer': 'https://app-api.pixiv.net/'})
    return img.content


def get_pixiv_detail(api, illust_id):
    """
    获取pixiv详情
    返回pixiv详情json数据
    """
    pixiv_detail = api.illust_detail(illust_id)
    return pixiv_detail

#a=(get_ranking(pixiv_login()))
#pass
#download_illust('https://i.pximg.net/c/600x1200_90/img-master/img/2022/07/10/15/15/47/99628080_p0_master1200.jpg')
