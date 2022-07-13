# SetuBot 色图机器人
使用telegram查看色图

新增pixiv功能！
## 使用公开机器人（不保证可用性）
1. https://t.me/tbSetubot 跳转到telegram打开机器人
2. 输入/start 开始使用
3. 输入/setu 在数据库中所有色图中随机发送一张色图
4. 输入/setu r18 在数据库中所有色图中随机发送一张18禁色图
5. 输入/pixiv num=? 获取pixiv排行榜前num名的作品，num不写则为10
6. TODO：获取r18排行榜
## 自建机器人
1. 克隆代码
2. 创建token.txt文件，内容为你的机器人token，格式为：
```
123456:abcdefgh
```
3. 自行获取pixiv的REFRESH_TOKEN，并写入pixiv_token.txt文件中，获取方法参见https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde
4. 安装`requirements.txt`中的库
5. 运行start.py

## 问题
已知在非中文操作系统上运行会出现Unicode Decode错误，疑为PyTelgramBotAPI的问题，不准备修了。
## 鸣谢
1. [Telegram](https://telegram.org/)
2. [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
3. [cloudscraper](https://github.com/VeNoMouS/cloudscraper)
4. [pycharm](https://www.jetbrains.com/pycharm/)
5. [色图api](https://github.com/yuban10703/SetuAPI)
6. [pixiv](https://www.pixiv.net/)
7. [pixivpy](https://github.com/upbit/pixivpy)
## 打赏
本项目完全免费且公开提供，如果你喜欢这个项目，请赏作者一杯咖啡！
![支付宝红包码](./hongbaoma.jpg)
![支付宝](./zfb.jpg)