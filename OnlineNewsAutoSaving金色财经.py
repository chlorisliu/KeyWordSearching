import requests
from bs4 import BeautifulSoup
import re
import schedule
import time


def getNewsInfoOnline():
    newsInfo = [['Time','Title','Source','Summary']]
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36'}
    
    url1 = 'https://www.jinse.cn/'
    res1 = requests.get(url1, headers=headers).text
    p_info1 = '<section class="js-article_item" data-v-a31badcc>(.*?)</a>'
    info1 = re.findall(p_info1, res1, re.S)
    pattern1 = r'<a\s+href="(.*?)"\s+title="(.*?)"'
    p_info4 = '</span></a> (.*?)<span class="js-article_item__foot--pageview" data-v-a31badcc>'
    info4 = re.findall(p_info4, res1, re.S)
    pattern4 = r'<p class="js-article_item__des" data-v-a31badcc>\s+(.*?)\s+</p></div> <div class="js-article_item__foot" data-v-a31badcc><a href="/member/.*?" title=".*?" target="_blank" class="js-article_item__foot-author" data-v-a31badcc>\s+(.*?)\s+</a> <span class="js-article_item__foot--time" data-v-a31badcc> · (.*?)</span>'

    for article in info1:
        match = re.search(pattern1, article)
        if match:
            link = match.group(1)
            title = match.group(2)
            print("Source:", link)
            print("Title:", title)
            print()
            newsInfo.append([None,title,link,None])
        
    for article in info4:
        match = re.search(pattern4, article)
        if match:
            title = match.group(1)
            source = match.group(2)
            time = match.group(3)
            print(f"Title: {title}")
            print(f"Source: {source}")
            print(f"Time: {time}")
            print()
            newsInfo.append([time,title,source,None])

    url2 = "https://www.jinse.cn/lives"
    res2 = requests.get(url2, headers=headers).text
    p_info2 = '<div class="time">\n\n (.*?)</a> <!----></div> <!----> <!----> <!---->'
    info2 = re.findall(p_info2, res2, re.S)
    pattern2 = r'(.*?)\n\s+</div> <div class="content"><!----> <a href="(.*?)" target="_blank" class="title"><!---->\n\s+(.*?)\n\s+</a> <!----> <a href=".*?" target="_blank" style="color: #767680">(.*?)</a>'
    for article in info2:
        match = re.search(pattern2, article)
        if match:
            time = match.group(1).strip()
            href = match.group(2)
            title = match.group(3)
            summary = match.group(4).strip()
            print(f'Time: {time}')
            print(f'Title: {title}')
            print(f'Source: {href}')
            print(f'Summary: {summary}')
            print()
            newsInfo.append([time,title,href,summary])
        
    url3 = "https://www.jinse.cn/industry"
    res3 = requests.get(url3, headers=headers).text
    p_info3 = '<p class="title" data-v-e74bab12>(.*?) </p>'
    info3 = re.findall(p_info3, res3, re.S)
    for article in info3:
        title = article.strip()
        print(f'Title: {title}')
        print()
        newsInfo.append([None,title,None,None])


    import csv
    # 设置保存文件路径和文件名
    csv_file = 'output.csv'

    # 打开 CSV 文件并写入数据
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(newsInfo)

    print("输出已保存为 CSV 文件：", csv_file)

schedule.every(0.01).hours.do(getNewsInfoOnline)  # 每隔##小时执行一次爬虫

while True:
    schedule.run_pending()
    time.sleep(0.01)


