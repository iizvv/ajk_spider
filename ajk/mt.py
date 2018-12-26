import requests
from scrapy.selector import Selector
import time
import csvUtils

headers = {
           "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "cookie": "",
           }

proxies = {
            # "https": "139.196.196.74:80",
            "http": "223.85.196.75:9999",
            }

def start():
    for i in range(1, 51):
        response = requests.get(url="http://bj.maitian.cn/esfall/PG"+str(i), headers=headers, proxies=proxies)
        selector = Selector(text=response.content)
        links = selector.css(".list_wrap .clearfix .hide_border a::attr(href)").extract()
        for link in links:
            url = "http://bj.maitian.cn/"+str(link.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", ""))
            print("当前为:" + str(i) + "页, 请求地址:" + url)
            getMsg(url)
            time.sleep(10)

# 获取信息
def getMsg(url):
    response = requests.get(url=url, headers=headers, proxies=proxies)
    selector = Selector(text=response.content)
    sale = getSalesName(selector)
    phone = getPhoneNumner(selector)
    if len(phone) == 11:
        print("姓名:" + sale + "\n手机号:" + phone)
        csvUtils.saveMsg("麦田销售信息", [sale, phone])

# 获取姓名
def getSalesName(selector):
    return str(selector.css(".top_jl ::text").extract_first())

# 获取手机号
def getPhoneNumner(selector):
    element = selector.css("#clickMobileTJ").extract_first()
    return element.split("phoneLogClick")[1].split(",")[0].replace("(", "").replace("'", "").replace(" ", "")

if __name__ == '__main__':
    start()
