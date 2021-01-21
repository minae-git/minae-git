from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import os
import time
import json
import pandas as pd
import login_info

# base url for requests
base_url = "https://www.instagram.com/"
login_url = base_url + "accounts/login/"
hash_base_url = base_url + "explore/tags/"


# headeless options for webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")

# Chrome webdriver instance : browser
# print(os.getcwd())
browser = webdriver.Chrome("./webdriver/chromedriver.exe")
browser.maximize_window()

# requests to instagram
browser.get("https://www.instagram.com/accounts/login/")


## Login process
browser.implicitly_wait(10)


login_form = browser.find_elements_by_xpath('//*[@id="loginForm"]//label[@class="f0n8F "]')
# print(len(login_form))
login_id, login_pw = login_form[0], login_form[1]

login_id.send_keys(login_info.insta_id)
login_pw.send_keys(login_info.insta_pw)
browser.implicitly_wait(3)

browser.find_element_by_xpath('//*[@id="loginForm"]//button').submit()
browser.implicitly_wait(10)

browser.find_element_by_css_selector("div.cmbtv > button").click()
browser.implicitly_wait(10)

# after_login_source = browser.page_source
# browser.save_screenshot("C:/Users/minae2324/Documents/crawling_pic/after_login.png")
# print(after_login_source)
# browser.implicitly_wait(10)


# 태그명 조합은 어떻게? -> 구, 동, 유명 명소/지명 + '맛집'(ex: 용산구 맛집, 남영동맛집, 경리단길맛집)
with open("./insta/seoul_district.json", 'r', encoding="utf-8") as file:
    seoul_district = json.load(file)

initial_search_tags = [district + "맛집" for district in seoul_district.keys()]
# print(initial_search_tags)

# 로그인 후 hashtag 검색 페이지로 이동
browser.get(hash_base_url + initial_search_tags[2] + "/") # 용산구맛집에 대해 크롤링
time.sleep(5) # 로딩까지 시간이 좀 걸리네요....

### main process -> location id, insta location name, hashtags, likes, text, date

# 처음 33개의 포스트만 불러오며, 이후 12개씩 추가로 불러옴
initial_feed_num = 33


# 이전의 time.sleep(5)로 최초 포스트 33개가 로딩되는지 확인
post_list = browser.find_elements_by_class_name("_bz0w")
# print(len(post_list), type(post_list))

marginal_num = 0


for post in post_list[23:27]:
    post.find_element_by_css_selector("a").click()
    # time.sleep(3)
    (WebDriverWait(browser, 3)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.RxpZH"))))

    browser.save_screenshot("C:/Users/minae2324/Documents/crawling_pic/{}_{}.png".format(
        initial_search_tags[2], 1))
    post_contents = browser.page_source

    # 여기서부터
    browser.find_element_by_css_selector("div.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button").click()
    browser.implicitly_wait(10)


    # if len(browser.find_elements_by_class_name("_bz0w")) > 

    new_post_list = browser.find_elements_by_class_name("_bz0w")
    print(len(new_post_list))
    time.sleep(3)

    # webdriver.ActionChains(browser).move_to_element()

#     browser.



    
# soup = BeautifulSoup(browser.page_source, 'html.parser')
# soup.select("div.KL4Bh > img")





# Closing webdriver
browser.close()