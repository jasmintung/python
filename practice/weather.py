import requests
import json
import time


class Check_pm_health(object):
    today_time = time.strftime("%Y%m%d", time.localtime())

    def __init__(self, weaid):
        self.weaid = weaid  # 城市ＩＤ
        self.params = {
            'app': 'weather.history',
            'appkey': '10003',
            'weaid': self.weaid,  # bj:101010100 ,sh:101020100
            'date': self.today_time,
            'sign': 'b59bc3ef6191eb9f747dd4e83c99f2a4',
            'format': 'json',

        }

    @property
    def test(self):  # 默认查询上海天气/也可以更具当前的地理位置查询当前所在的天气
        result = requests.get(params=self.params, url="http://api.k780.com:88")  # params url post 参数
        a = result.json()
        json.dump(a, open("wather.json", "w", encoding="utf8"), indent=4, ensure_ascii=False)
        b = a.get("result")
        print((b[0]['aqi']))  # 返回当天的天气值

    @test.setter
    def test(self, newcity):  # 自定义天气查询
        self.params['weaid'] = newcity
        self.test


a = Check_pm_health(101010100)
a.test
a.test = 101020100