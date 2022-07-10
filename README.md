# SetuBot 色图机器人
使用telegram查看色图
## 使用公开机器人（不保证可用性）
1. https://t.me/tbSetubot 跳转到telegram打开机器人
2. 输入/start 开始使用
3. 输入/setu 在数据库中所有色图中随机发送一张色图
4. 输入/setu r18 在数据库中所有色图中随机发送一张18禁色图

## 自建机器人
1. 克隆代码
2. 创建token.txt文件，内容为你的机器人token，格式为：
```
123456:abcdefgh
```
3. 安装pyTelegramBotAPI和cloudscraper库
4. 运行start.py

## 问题
已知在非中文操作系统上运行会出现Unicode Decode错误，疑为PyTelgramBotAPI的问题，不准备修了。
## 鸣谢
1. [Telegram](https://telegram.org/)
2. [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
3. [cloudscraper](https://github.com/VeNoMouS/cloudscraper)
4. [pycharm](https://www.jetbrains.com/pycharm/)
5. [色图api](https://github.com/yuban10703/SetuAPI)