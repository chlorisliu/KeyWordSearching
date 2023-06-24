import requests
from bs4 import BeautifulSoup
import schedule
import time

def search_websites(keyword, website_urls):
    for url in website_urls:
        # 发起HTTP GET请求获取网页内容
        response = requests.get(url)
        content = response.text
        
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(content, 'html.parser')
        
        # 在网页中查找含有关键词的链接和标题
        articles = soup.find_all('a')
        for article in articles:
            if keyword in article.text:
                article_title = article.text
                article_link = article['href']
                print("网站：", url)
                print("文章标题：", article_title)
                print("文章链接：", article_link)
                print()

# 指定关键词和多个网站URL

def run_crawler():
    # 在这里替换为你要搜索的网址和关键词
    website_urls = [
    "https://www.panewslab.com/",
    "https://www.odaily.news/",
    "https://blockcast.it/",
    "https://www.cebnet.com.cn/blockchain/",
    'https://www.8btc.com/',
    "https://cointelegraph.com/",
    "https://www.jinse.cn/"
]
    keyword = "BTC"

    for website in website_urls:
        search_websites(keyword, website_urls)
        print("=======================================")
# 设置定时任务

schedule.every(0.001).hours.do(run_crawler)  # 每隔##小时执行一次爬虫
while True:
    schedule.run_pending()
    time.sleep(0.001)


