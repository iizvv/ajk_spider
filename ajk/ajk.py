import requests
from scrapy.selector import Selector
import time
import csv

headers = {
           "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
           }

def start():
    for i in range(1, 100):
        ajk_url = "https://tianjin.anjuke.com/sale/p" + str(i)
        response = requests.get(url=ajk_url, headers=headers)
        selector = Selector(text=response.text)
        links = selector.css(u'.list-item a::attr(href)').extract()
        for link in links:
            print("当前为:" + str(i) + "页")
            getMessage(link)
            time.sleep(1)


# 获取信息
def getMessage(url):
    # 设置cookie启动即可开始抓取
    headers["cookie"] = ""
    response = requests.get(url=url, headers=headers)
    selector = Selector(text=response.text)
    sales = getSalesName(selector)
    phone = getPhoneNumber(response)
    company = getCompanyName(selector)
    store = getStoreName(selector)
    print("请求地址:" + url + "\n姓名:" + sales + "\n手机号:" + phone + "\n公司名:" + company + "\n门店名:" + store)
    saveMessage([sales, phone, company, store])


# 保存信息
def saveMessage(info):
    with open('天津地区安居客二手房模块销售人员信息.csv', 'a+', newline="") as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(info)


# 获取销售名
def getSalesName(selector):
    return selector.css(".brokercard-name ::text").extract_first().replace(" ", "")


# 获取公司名
def getCompanyName(selector):
    return selector.css(".broker-company a::attr(title)").extract_first().replace("工商注册名称:", "")


# 获取门店名
def getStoreName(selector):
    return selector.css(".broker-company a::text").extract()[1].replace("...", "")


# 获取销售手机号
def getPhoneNumber(response):
    return ajx(getParams(response))


# 获取销售手机号请求参数
def getParams(response):
    keys = ["broker_id", "token", "prop_id", "prop_city_id", "house_type"]
    params = dict()
    re = response.text.split("InquirePhoneNum")
    if len(re) >= 1:
        re = re[1].split("});")[0].replace("'", "").replace("\n", "").replace(" ", "").replace("(", "").replace("{", "")
        for temp in re.split(","):
            kv = temp.split(":")
            if kv[0] in keys:
                params[kv[0]] = kv[1]
    params["captcha"] = ""
    return params


# 获取销售手机号的请求
def ajx(params):
    response = requests.get(url="https://beijing.anjuke.com/v3/ajax/broker/phone/", headers=headers, params=params)
    li = response.text.split(":")
    return li[len(li) - 1].replace(" ", "").replace("'", "").replace("}", "").replace("\"", "")

if __name__ == '__main__':
    start()
