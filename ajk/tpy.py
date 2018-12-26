import requests
from scrapy.selector import Selector
import time
import csv

headers = {
           "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "cookie": "",
           }

def start():
    for i in range(0, 50):
        tpy_url = "https://taipingyangfang.anjuke.com/gongsi-esf/p" + str(i) + "/#filtersort"
        response = requests.get(url=tpy_url, headers=headers)
        selector = Selector(text=response.content)
        links = selector.css(".houselist-mod-new a::attr(href)").extract()
        for link in links:
            print("\n当前为:" + str(i) + "页, 请求地址:" + link)
            getMessage(link)
            time.sleep(1)

# 获取信息
def getMessage(url):
    response = requests.get(url=url, headers=headers)
    selector = Selector(text=response.content)
    sale = getSalesName(selector)
    company = getCompanyName(selector)
    store = getStoreName(selector)
    phone = getPhoneNumber(response)
    if len(phone) == 11:
        print("姓名:" + sale + "\n手机号:" + phone + "\n公司名:" + company + "\n门店名:" + store)
        saveMessage([sale, phone, company, store])

# 保存信息
def saveMessage(info):
    with open('上海太平洋房销售信息.csv', 'a+', newline="") as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(info)

# 获取销售名
def getSalesName(selector):
    return str(selector.css(".hd ::text").extract_first()).replace("\"", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "").replace("的店铺", "")

# 获取公司名
def getCompanyName(selector):
    return str(selector.css(".msg-wrap a::text").extract_first())

# 获取门店名
def getStoreName(selector):
    re = selector.css(".msg-wrap a::text").extract()
    if len(re) >= 2:
        return str(selector.css(".msg-wrap a::text").extract()[1])
    return ""

# 获取手机号
def getPhoneNumber(response):
    return ajx(getParams(response))

# 获取销售手机号请求参数
def getParams(response):
    keys = ["broker_id", "token", "prop_city_id"]
    params = dict()
    re = response.text.split("getBrokerPhone")
    if len(re) >= 1:
        re = re[1].split("});")[0].replace("'", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "").replace("(", "").replace("{", "").split(",")
        for r in re:
            kv = r.split(":")
            if kv[0] in keys:
                params[kv[0]] = kv[1]
        params["captcha"] = ""
        return params

# 获取销售手机号的请求
def ajx(params):
    url = "https://taipingyangfang.anjuke.com/v3/ajax/broker/phone/"
    response = requests.get(url, headers=headers, params=params)
    li = response.text.split(":")
    return li[len(li) - 1].replace(" ", "").replace("'", "").replace("}", "").replace("\"", "")


if __name__ == '__main__':
    start()
