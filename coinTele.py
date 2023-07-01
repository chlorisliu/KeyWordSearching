import time
import pandas as pd
from selenium import webdriver 
from selenium.webdriver import ActionChains
from tqdm import tqdm
from selenium.webdriver.common.by import By
import pandas as pd
from openpyxl import Workbook
import csv
import subprocess


chrome_driver_path = '/Users/chlorisliu/Downloads/chromedriver_mac_arm64' ###local path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')

# Provide 'options' argument only once when initializing WebDriver
browser = webdriver.Chrome(options=chrome_options)

url: str = input("enter the link to scrape: \n")
file_name: str = input("enter the name of the file name: \n")
num_pages: int = input("number of pages to scrape: \n")

def get_title(element):
    return element.find_element(By.CLASS_NAME,"post-card-inline__title").text


def get_date(element):
    return element.find_element(By.TAG_NAME,"time").get_attribute("datetime")


def get_author_profile(element):
    return element.find_element(By.CLASS_NAME,"post-card-inline__author").find_element(By.TAG_NAME,
        "a").get_attribute("href")


def get_author(element):
    return element.find_element(By.CLASS_NAME,"post-card-inline__author").find_element(By.TAG_NAME,
        "a").text


def summary_text(element):
    return element.find_element(By.CLASS_NAME,"post-card-inline__text").text


def get_views(element):
    return element.find_element(By.CLASS_NAME,"post-card-inline__stats").text


def get_news_url(element):
    return element.find_element(By.TAG_NAME,"a").get_attribute("href")


if __name__ == '__main__':

    browser.get(url)

    for i in tqdm(range(0, int(num_pages))):
        time.sleep(2)
        browser.execute_script("scrollBy(0,10000);")
        button = browser.find_element(By.CLASS_NAME,"posts-listing__more-wrp")
        ActionChains(browser).click(button).perform()

    time.sleep(2)
    news_titles = browser.find_elements(By.CLASS_NAME,"post-card-inline__content")

    news = [['titleText', 'articleDate', 'authorProfile', 'authorName', 'Summary', 'Views', 'URL']]
    for item in tqdm(news_titles):
        titleText = get_title(item)
        articleDate = get_date(item)
        authorProfile = get_author_profile(item)
        authorName = get_author(item)
        summary = summary_text(item)
        views = get_views(item)
        url = get_news_url(item)
        info = [titleText,
                articleDate,
                authorProfile,
                authorName,
                summary,
                views,
                url]

        news.append(info)
        
    
    offcialFileName = file_name + ".csv"
    workbook = Workbook()
    sheet = workbook.active

# 将2D列表的数据写入工作表
    with open(offcialFileName, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in news:
            writer.writerow(row)

# 从CSV文件中读取数据并将其写入Excel工作表
    with open(offcialFileName, 'r') as file:
        reader = csv.reader(file)
        for row_index, row in enumerate(reader, start=1):
            for column_index, value in enumerate(row, start=1):
                sheet.cell(row=row_index, column=column_index).value = value

    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    # 保存Excel文件
    workbook.save(offcialFileName)
    subprocess.Popen(['open', offcialFileName])


    browser.close()
