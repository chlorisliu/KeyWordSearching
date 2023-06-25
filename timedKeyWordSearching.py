import requests
from bs4 import BeautifulSoup
import re
import schedule
import time

def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_page(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
    return elements

def search_keyword(url, keyword):
    html = get_page(url)
    if html:
        elements = parse_page(html, keyword)
        if elements:
            for element in elements:
                link = '<a href="' + url + '">' + url + '</a>'
                print("关键词: {}, 链接: {}".format(element, link))
        else:
            print("Not Found")
    else:
        print("无法获取网页内容。")

def run_crawler():
    url = "https://www.jinse.cn/"
    keyword = "SEC"

    search_keyword(url, keyword)

# 设置定时任务
schedule.every(0.001).hours.do(run_crawler)  # 每隔##小时执行一次爬虫

while True:
    schedule.run_pending()
    time.sleep(0.001)
