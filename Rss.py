import json
from urllib.parse import quote
from Lib.Network import Network
from Lib.ini import CONF


class RSS():
    sec = "RSS"
    hour = "*/1"
    minute = "30"
    wait = 5
    "订阅更新间隔"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        self.s = n
        self.c = c

    def rss(self, url):
        return self.s.get(f"https://api.rss2json.com/v1/api.json?rss_url={quote(url)}")

    def cache(self, url, data: str = ""):
        if data == "":
            # 在ini无法输入%之前采用的暴力措施
            # return base64.b64decode(bytes(self.c.load(self.sec, quote(url))[0], encoding='utf-8')).decode()
            return self.c.load(self.sec, quote(url))[0]
        else:
            # self.c.add(self.sec, quote(url), base64.b64encode(data.encode('utf8')).decode())
            self.c.add(self.sec, quote(url), data)
            self.c.save()

    def subscribe(self, data):
        all = self.c.load(self.sec, "subscribe")[0]
        if all == False:
            all = []
        else:
            all = json.loads(all)
        if data not in all:
            all.append(data)
            self.c.add(self.sec, "subscribe", json.dumps(all))
            self.c.save()
            return True
        return False

    def unsubscribe(self, data):
        all = self.c.load(self.sec, "subscribe")[0]
        all = json.loads(all)
        try:
            all.remove(data)
        except Exception:
            return False
        self.c.remove(self.sec, data["word"])
        self.c.add(self.sec, "subscribe", json.dumps(all))
        self.c.save()
        return True

    def showsubscribe(self):
        all = self.c.load(self.sec, "subscribe")[0]
        if all == False:
            all = []
        else:
            all = json.loads(all)
        return all

    def analysis(self, url):
        "重点重构对象,提取缓存与实时RSS订阅的内容区别,即更新的内容"
        return self.rss(url).json()

    def transform(self, data, msg=""):
        "重点重构对象,将更新的条目整合成一条消息,返回MesssagePart或其可兼容值"
        return data

    def Timer(self):
        '''需要定时器的功能,返回值为空列表或\n        
        [{
            "function": callable,
            "cron": {
                "hour": "*/12",
                "minute": "*"
            }
        }]'''
        return []

    def start(self):
        '''预加载的功能,返回值为空列表或\n        
        [callable1,callable2]'''
        return []

    def search(self, word):
        "实现搜索功能,正常应该返回MessageChain或其可兼容值"


class RSSException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Acgnx(RSS):
    sec = "Acgnx"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        super().__init__(n, c)

    def rss(self, word):
        url = f"https://share.acgnx.net/rss.xml?keyword={word}"
        return super().rss(url)

    def cache(self, word, data: json = {"items": [{"title": ""}]}):
        return super().cache(word, data["items"][0]["title"])

    def analysis(self, word):
        old = self.cache(word)
        new = self.rss(word).json()
        if new["items"] == []:  # 获取内容为空,代表着未初始化
            self.cache(word, {"items": [{"title": []}]})
            return new
        if old == "[]":  # 缓存为空,获取内容不为空,即订阅更新
            self.cache(word, new)
            return new
        if old == False:  # 初始化订阅
            self.cache(word, new)
            new["items"] = []
            return new
        else:
            diff = []
            for i in new["items"]:
                if i["title"] == old:
                    self.cache(word, new)
                    new["items"] = diff
                    return new
                else:
                    diff.append(i)
            # 未能匹配到缓存中的更新时间,即长时间未获取更新,更新列表过长直接忽略
            self.cache(word, new)
            new["items"] = []
            return new

    def transform(self, new: json, msg="叮叮,侦测到订阅更新\n"):
        if new["items"] == []:
            return False
        msg = f"{msg}{new['feed']['title']}\n\n"
        for i in new["items"]:
            msg += f"{i['categories'][0]} {i['title']}\n{i['link'].replace('https://share.acgnx.se','https://share.acgnx.net')}\n\n"
        return msg[:-2]

    def search(self, word):
        return self.transform(self.rss(word), msg="")


if __name__ == "__main__":
    a = Acgnx(Network({}, log_level=10))
    subscribe = ["無神世界的神明活動 ANi baha"]
    subscribe = {
        "無神世界的神明活動 ANi baha": "Upload/a"
    }

    fin = []
    for i in subscribe:
        tmp = a.analysis(quote(i))
        if tmp["items"] != []:
            for j in tmp["items"]:
                fin.append(
                    {"link": j["enclosure"]["link"], "Upload": subscribe[i]})

    with open("rss.log", "w") as f:
        json.dump(fin, f)
