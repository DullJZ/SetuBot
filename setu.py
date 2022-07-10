import json
import cloudscraper

setu_api = r"https://setuapi.dulljz666.workers.dev/setu"


def fetch_setu(r18=2, num=1):
    tmp1 = cloudscraper.create_scraper()
    tmp2 = tmp1.get(setu_api+"?r18="+str(r18)+"&num="+str(num))
    return json.loads(tmp2.content)


