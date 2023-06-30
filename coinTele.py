import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver as wd

chrome_driver_path = '/Users/chlorisliu/Downloads/chromedriver_mac_arm64'
chrome_options = wd.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')

# Provide 'options' argument only once when initializing WebDriver
browser = webdriver.Chrome(options=chrome_options)

url = input("Enter the link to scrape: ")
file_name = input("Enter the name of the output file: ")
num_pages = int(input("Enter the number of pages to scrape: "))

url = "https://cointelegraph.com/"


def get_title(element):
    return element.find_element_by_class_name("post-card-inline__title").text

def get_date(element):
    return element.find_element_by_tag_name("time").get_attribute("datetime")

def get_author_profile(element):
    return element.find_element_by_class_name("post-card-inline__author").find_element_by_tag_name("a").get_attribute("href")

def get_author(element):
    return element.find_element_by_class_name("post-card-inline__author").find_element_by_tag_name("a").text

def summary_text(element):
    return element.find_element_by_class_name("post-card-inline__text").text

def get_views(element):
    return element.find_element_by_class_name("post-card-inline__stats").text

def get_news_url(element):
    return element.find_element_by_tag_name("a").get_attribute("href")

browser.get(url)

for i in tqdm(range(num_pages)):
    browser.get(url)
    time.sleep(3)
    browser.execute_script("scrollBy(0,10000);")
    button = browser.find_element_by_class_name("posts-listing__more-wrp")
    ActionChains(browser).click(button).perform()

time.sleep(3)
news_titles = browser.find_elements_by_class_name("post-card-inline__content")

news = []
for item in tqdm(news_titles):
    title_text = get_title(item)
    article_date = get_date(item)
    author_profile = get_author_profile(item)
    author_name = get_author(item)
    summary = summary_text(item)
    views = get_views(item)
    url = get_news_url(item)
    info = [title_text, article_date, author_profile, author_name, summary, views, url]
    news.append(info)

news_df = pd.DataFrame(news, columns=["title_text", "article_date", "author_profile", "author_name", "summary", "views", "url"])
news_df.to_csv(file_name, index=False)

browser.close()