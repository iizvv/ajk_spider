import requests
from scrapy.selector import Selector
import time
import csvUtils

headers = {
           "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "cookie": "",
           }

def start():
    for i in range(0, 52):
        ajk_url = "https://tianjin.anjuke.com/sale/p" + str(i)
        response = requests.get(url=ajk_url, headers=headers)
        selector = Selector(text=response.text)
        links = selector.css(u'.list-item a::attr(href)').extract()
        for link in links:
            print("\n当前为:" + str(i) + "页, 请求地址:" + link)
            getMessage(link)
            time.sleep(1)


# 获取信息
def getMessage(url):
    response = requests.get(url=url, headers=headers)
    selector = Selector(text=response.text)
    sales = getSalesName(selector)
    phone = getPhoneNumber(response)
    company = getCompanyName(selector)
    store = getStoreName(selector)
    print("姓名:" + sales + "\n手机号:" + phone + "\n公司名:" + company + "\n门店名:" + store)
    csvUtils.saveMsg("安居客", [sales, phone, company, store])


# 获取销售名
def getSalesName(selector):
    return str(selector.css(".brokercard-name ::text").extract_first()).replace(" ", "")


# 获取公司名
def getCompanyName(selector):
    return str(selector.css(".broker-company a::attr(title)").extract_first()).replace("工商注册名称:", "")


# 获取门店名
def getStoreName(selector):
    return str(selector.css(".broker-company a::text").extract()[1]).replace("...", "")


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
