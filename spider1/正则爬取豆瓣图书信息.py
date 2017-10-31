# coding:utf-8
# 正则有点问题。但是没有报错。
import requests
import re

# 爬取内容
try:
    result= requests.get("https://book.douban.com/").text
    # print(type(result))
    # print(result)

    # print("获取信息")
    # re1=re.compile('<li.*?img src="(.*?)".*?"author">(.*?)<div>.*?"title">(.*?)<.*?"year">(.*?)<.*?<li>',re.S)
    re1=re.compile('<li.*?src="(.*?)".*?"author">(.*?)<.*?"title">(.*?)<.*?</li>',re.S)
    result1=re.findall(re1,result)
    print("输出结果")
    print(result1)
except Exception as e:
    print("cuowu")
    print(e)

