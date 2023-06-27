import requests
from bs4 import BeautifulSoup
import re
import schedule
import time
import pandas as pd
from openpyxl import Workbook
import csv
from openpyxl import Workbook
import subprocess

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
    pattern2 = r'(.*?)\n\s+</div> <div class="content"><!----> <a href="(.*?)" target="_blank" class="title"><!---->\n\s+(.*?)\n\s+</a> <!----> <a href=".*?" target="_blank" style="color: #.*?">(.*?)</a>'
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

    filename = 'output.xlsx'
# 创建一个新的工作簿
    workbook = Workbook()
    sheet = workbook.active

# 将2D列表的数据写入工作表
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in newsInfo:
            writer.writerow(row)

# 从CSV文件中读取数据并将其写入Excel工作表
    with open('output.csv', 'r') as file:
        reader = csv.reader(file)
        for row_index, row in enumerate(reader, start=1):
            for column_index, value in enumerate(row, start=1):
                sheet.cell(row=row_index, column=column_index).value = value

    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    # 保存Excel文件
    workbook.save(filename)
    filename = 'output.xlsx'
    subprocess.Popen(['open', filename])

schedule.every(0.0001).hours.do(getNewsInfoOnline)  # 每隔##小时执行一次爬虫

while True:
    schedule.run_pending()
    time.sleep(0.001)


