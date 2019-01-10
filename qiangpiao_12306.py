from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import re
import lxml
from lxml.html import etree

# 简单完成一般，写的乱七八糟。
# 为了练习selenium
# 现有界面，后无界面，
# 思路是先模拟登录,,用selenium打开页面后，提取图片，认为分析，然后输入符合图片的序号，为1234，下面为5678
# 输入结束后哎页面中会模拟1234,5678做一个偏移量的点击操作
# 登陆后，就可以selenium模拟后面的操作了。这种情况下是带cookie，所以可以提交信息。

'''
1.大概过程是：
    1.写好配置，或者启动时候配置
    2.启动文件
    3.需要输入验证码的时候，输入图片的序列，查看截图verify_img.png
    4.如果成功，将会进入到12306自动买票阶段了
    5.如果不成功，就继续进行验证码验证
'''

# 这里是全局配置：
# 配置方面不够：需要起始站，终点站，车名，cookies，查询时间，座位，名字
START_STATION = '北京西'
END_STATION = '长治'
QUERY_TIME = '2019-01-16'
COOKIES = 'tk=hCbU1bzjmIfSLOmdlAuf933NTbFuNwquDhotsGsDFQ04fZ5b451110; JSESSIONID=667C224E267A3E201BA0B956ACDD9DF0; RAIL_EXPIRATION=1547237157204; RAIL_DEVICEID=C8ysc3sa0-SY0csr612fgAFbvwoU7ZeQTIGQ5JTxh3Q-WBnOmOjtusXlZCAEA-Orx0elImHhAi_s06DXmKvJ6JTMw_dvfdMZmAFBU7flA5IJvzzLggDSjWwFXdtMac5zGpHQSr2BV9e875K9oOP65s76mgDLe6pr; _jc_save_wfdc_flag=dc; _jc_save_zwdch_cxlx=1; _jc_save_zwdch_fromStation=%u90AF%u90F8%2CHDP; BIGipServerportal=3151233290.17695.0000; BIGipServerpool_passport=267190794.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toDate=2019-01-09; BIGipServerpassport=971505930.50215.0000; _jc_save_toStation=%u957F%u6CBB%u5317%2CCBF; searchHistory=%5B%7B%22innerText%22%3A%22k163%22%7D%5D; current_captcha_type=Z; _jc_save_fromDate=2019-01-09; BIGipServerotn=1927807242.64545.0000'
STATION_NAME = 'K1163'
SEAT_TYPE = ''
PASSENGER_NAME = ''
USERNAME = ''
PASSWORD = ''

# 全局的driver变量
driver = webdriver.Chrome()
# 隐式等待
driver.implicitly_wait(10)
driver.maximize_window()

# 后面不需要了
def parse_cookies(cookies_str):
    # cookies_str = '''JSESSIONID=680A7E3D4E33AFDDD367D49596901C53; RAIL_EXPIRATION=1547237157204; RAIL_DEVICEID=C8ysc3sa0-SY0csr612fgAFbvwoU7ZeQTIGQ5JTxh3Q-WBnOmOjtusXlZCAEA-Orx0elImHhAi_s06DXmKvJ6JTMw_dvfdMZmAFBU7flA5IJvzzLggDSjWwFXdtMac5zGpHQSr2BV9e875K9oOP65s76mgDLe6pr; _jc_save_wfdc_flag=dc; _jc_save_zwdch_cxlx=1; _jc_save_zwdch_fromStation=%u90AF%u90F8%2CHDP; BIGipServerportal=3151233290.17695.0000; BIGipServerpool_passport=267190794.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=401605130.38945.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u957F%u6CBB%u5317%2CCBF; _jc_save_fromDate=2019-01-10; _jc_save_toDate=2019-01-09'''
    '''将输入的cookies进行格式化，适合进行请求'''
    cookies_dict = {}
    all_cookies_list = []
    if cookies_str:
        cookies_list = cookies_str.split(';')
        for i in cookies_list:
            i_list = i.strip().split('=')
            # if i_list[0] == 'tk':
            cookies_dict['name']=i_list[0]
            cookies_dict['domain'] = 'kyfw.12306.cn'
            cookies_dict['value'] = i_list[1]
            all_cookies_list.append(cookies_dict)
        print(all_cookies_list)
        return all_cookies_list
    else:
        return None
def query_train_balance(start,end,querytime,station_name):
    '''
    查询车票余额页面，并且点击预定，然后提交信息。
    :param start: 格式为北京,BJP
    :param end:
    :param time:时间2019-1-31
    :return:
    '''
    url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={}&ts={}&date={}&flag=N,N,Y'.format(start,end,querytime)
    print('请求连接:'+ url)

    driver.get(url)
    # 这边需要携带登录后的cookies
    # print(driver.get_cookies())
    # for cookie in cookies_list:
    #     driver.add_cookie(cookie)
    ticket_list = driver.find_elements_by_xpath('//tr[contains(@id,"ticket")]')
    html = driver.page_source
    html_response = etree.HTML(html)
    ticket_list = html_response.xpath('//tr[contains(@id,"ticket")]')
    for ticket in ticket_list:
        print(ticket.xpath('.//td/div/div/div/a/text()'))
        if ticket.xpath('.//td/div/div/div/a/text()') and ticket.xpath('.//td/div/div/div/a/text()')[0]==station_name:
            # 硬座是10，软座是9，硬卧是8.等等还有其他选择
            print(ticket.xpath('.//td[10]/text()'))
            if ticket.xpath('.//td[8]/text()') and ticket.xpath('.//td[10]/text()')[0] == '有':
                print('找到火车票了')
                ticket_id = ticket.xpath('./@id')[0]
                click_button = driver.find_element_by_xpath('//tr[@id="{}"]//td[13]/a'.format(ticket_id))
                click_button.click()
                time.sleep(10)
                # 提交页面内容
                # 我这里默认提交第一个了,如果需要就遍历
                input_button = driver.find_element_by_id('normalPassenger_0')
                input_button.click()
                submit_button = driver.find_element_by_id('submitOrder_id')
                submit_button.click()
                get_verify_img('queren_success.png')
                # # 之后会弹出确认订单的页面：
                # queren_button = driver.find_element_by_id('qr_submit_id')
                # queren_button.click()
                print('买票成功')
                # # 到了这一步就能发送邮件了。
            else:
                print('没找到票')
        else:
            print('没找到车次')
    # 狐疑driver不能关闭
    #driver.close()


def get_map(chinastr,**kwargs):
    '''
    输入中文站，输入对应的大写。
    :param chinastr:
    :return:
    '''
    print('查找站名对应字母{}'.format(chinastr))
    if chinastr in kwargs.keys():
        print('查找站名对应结果{}:{}'.format(chinastr,kwargs.get(chinastr)))
        return ','.join([chinastr,kwargs.get(chinastr)])
    else:
        raise ValueError('找不到对应关系请重新输入')


def parse_map():
    '''
    每次都重新解析
    :return:
    '''
    # station_version的版本可能会导致对应输入的不同。
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9090'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}
    i = 0
    while i < 3:
        try:
            print('该链接正在请求:' + url)
            response = requests.get(url, headers=headers, allow_redirects=False,timeout=10)
            if response.status_code == 200:
                station_dict = parse_response(response)
                return station_dict
            else:
                time.sleep(30)
                i += 1
        except Exception as e:
            print('链接请求出错：' + url + str(e))
            time.sleep(30)
            i += 1
    raise ValueError('获取对应关系失败')

def parse_response(response):
    '''解析station列表'''
    print('开始解析station')
    station_dict = {}
    response_str = response.text
    pattern = re.compile("var station_names ='(.*?)';",re.S)
    if re.search(pattern, response_str):
        station_str = re.search(pattern, response_str).group(1)
        station_list = station_str.split('|')
        for i in range(0,len(station_list)-1, 5):
            station_dict[station_list[i+1]] = station_list[i+2]
        print('解析station完成')
        return station_dict
    else:
        raise ValueError('解析station对应关系失败')

# 配置方面不够：需要起始站，终点站，车名，cookies，查询时间，座位，名字
def main():
    # 定时任务额外做
    # 两种配置方法：一种输入，一种配置文件。
    start_station = input('请输入起始站：')
    end_station = input('请输入终点站：')
    station_name = input('请输入车次名称：')
    query_time = input('请输入查询的时间：')
    cookies = input('请输入cookies：')
    username = input('输入用户名密码：')
    password = input('输入密码：')
    if start_station and end_station and query_time and cookies:
        pass
    else:
        start_station = START_STATION
        end_station = END_STATION
        station_name = STATION_NAME
        query_time = QUERY_TIME
        cookies = COOKIES
        username = USERNAME
        password = PASSWORD

    try:
        print('准备登录：')
        to_login(username,password)
        station_dict = parse_map()
        while True:
            query_train_balance(get_map(start_station, **station_dict),get_map(end_station, **station_dict),query_time,station_name)
            time.sleep(120)
    except Exception as e:
        print('发生错误：{}'.format(str(e)))

def to_login(user, password):
    '''这一步整个流程是通了，但是有异常没有处理，暂时就搞到这了。'''
    url = 'https://kyfw.12306.cn/otn/resources/login.html'
    driver.get(url)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()
    driver.find_element_by_id('J-userName').send_keys(user)
    time.sleep(1)
    driver.find_element_by_id('J-password').send_keys(password)
    i = 1
    while i<5:
        verify_img = driver.find_element_by_id('J-loginImg')
        code = [[40,70], [110,70], [180,70], [250,70], [40,140], [110,140], [180,140], [250,140]]
        # verify_img.click()
        get_verify_img('verify_img.png')
        # 接受人工输入的image列表
        input_list = eval(input('请输入需要点击的图片序列（list）：'))

        code_list = [code[i-1] for i in input_list]
        # 依照偏移量点击事件
        for code_i in code_list:
            # 这一这边是一个点击一个实例化。
            action = ActionChains(driver)
            action.move_to_element_with_offset(verify_img,code_i[0],code_i[1]).click().perform()
            time.sleep(1)

        submit_button = driver.find_element_by_id('J-login')
        submit_button.click()
        try:
            html = driver.find_element_by_class_name('welcome-name')
            if html.text != '':
                print(html.text)
                print('登录成功')
                get_verify_img('login_success.png')
                return
        except Exception as e:
            print('登录失败,再次尝试：')
    raise TypeError('尝试登录失败，请重新启动')


def get_verify_img(imgpath):
    '''为了防止图片是变动的，只截取其中一部分图片，也可以全部截取,然后认为输入进去'''
    driver.save_screenshot(imgpath)
    # driver.get_screenshot_as_base64()
    # 直截取一部分是通过定位元素然后吧元素的大小通过pil截出来



if __name__=="__main__":
    main()