import requests
from scrapy.selector import Selector
import time
import csv

headers = {
           "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
           }

def start():
    for i in range(41, 100):
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
    headers["cookie"] = "aQQ_ajkguid=8043FF4E-B251-35DD-61BF-F443326ECF81; ctid=14; _ga=GA1.2.1450998270.1545699543; _gid=GA1.2.953326896.1545699543; wmda_uuid=30d51eff0905cc7a1028674915f9261e; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; 58tj_uuid=8c48d825-4360-4c32-9a6b-83458ffbc29a; als=0; lps=http%3A%2F%2Fbeijing.anjuke.com%2F%7C; twe=2; sessid=61B0A77B-2208-AF0E-D766-B146B8177F7A; ajk_member_captcha=fae4f14199c1aebbf64295d9532ab5a5; browse_comm_ids=614761%7C117073; wmda_session_id_6289197098934=1545786258110-94b72979-43c8-3afa; init_refer=https%253A%252F%252Fbeijing.anjuke.com%252F; new_uv=7; new_session=0; propertys=pfsbds-pkbo6g_pg0u2x-pka759_; __xsptplusUT_8=1; _gat=1; __xsptplus8=8.7.1545786258.1545791273.26%234%7C%7C%7C%7C%7C%23%23ZOYUthJS7qxEtq7LuzXr3urgmsaSBxiY%23"
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
    with open('天津安居客销售信息.csv', 'a+', newline="") as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(info)


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
