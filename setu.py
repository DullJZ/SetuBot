import requests
import json

setu_api = r"https://setu.yuban10703.xyz/setu"


def fetch_setu(r18=2, num=1):
    tmp = requests.get(setu_api+"?r18="+str(r18)+"&num="+str(num))
    return json.loads(tmp.text)


