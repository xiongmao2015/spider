import requests
import re
from requests import RequestException
import json

# 注意这里的思路是先确定状态是否成功，成功后，就返回代码
# 不成功就none,然后是为了防止程序崩溃，添加异常处理try.except
# 文档中分析可以知道所有错误都继承RequestExcption.
def get_one_page(url):
    try:
        html_content=requests.get(url)
        if html_content.status_code==200:
            return html_content.text
        return None
    except RequestException as e:
        return None

# 分析这个网页，确定正则表达式的写法，re.S是为了让点.可以匹配任何字符，包括换行符之类的。
# 注意这边yield的好处
def parse_one_page(html):
    # pattern = re.compile('<div class="pl2">.*?<img src="(.*?)" width.*?alt="(.*?)" class>.*?</div>',re.S)
    pattern = re.compile('<table width="100%".*?<img src="(.*?)" width.*? alt="(.*?)" class.*?pl">(.*?)</p>.*?</div>',re.S)
    items = re.findall(pattern,html)
    for  item  in items:
        yield{
            "image":item[0],
            "title":item[1],
            "actor":item[2]
        }
#把内容保存到文件中。
def write_to_file(content):
    with open('result.txt','a') as f:
        f.write(json.dumps(content)+'\n')
        f.close()

def main():
    url="https://movie.douban.com/chart"
    html=get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__== "__main__":
    main()

