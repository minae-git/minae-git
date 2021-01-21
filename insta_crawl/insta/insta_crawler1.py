from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import os
import json
import time
import pandas as pd

import login_info as login


##### Setting webdriver headless & user-agent option
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=\
    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/87.0.4280.141 Safari/537.36")


### Webdriver instance : browser
browser = webdriver.Chrome("./webdriver/chromedriver.exe", options=chrome_options)


### URLs for requesting
base_url = "https://www.instagram.com/"
login_url = base_url + "accounts/login/"
crawl_url = base_url + "explore/tags/"


### Login Process for further crawling
browser.get(login_url)
(WebDriverWait(browser, 10)\
    .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input._2hvTZ.pexuQ.zyHYP"))))

browser.save_screenshot("C:/Users/minae2324/Documents/crawling_pic/before_login.png")

id_form = browser.find_element_by_name("username").send_keys(login.insta_id)
pw_form = browser.find_element_by_name("password").send_keys(login.insta_pw)
browser.find_element_by_xpath('//*[@id="loginForm"]//button').submit()
browser.implicitly_wait(10)

browser.find_element_by_css_selector("div.cmbtv > button").click()
browser.implicitly_wait(10)
browser.save_screenshot("C:/Users/minae2324/Documents/crawling_pic/after_login.png")


### Crawling Process

# extracting the initial search tags from seoul district : initial_search_tags
with open("./insta/seoul_district.json", 'r', encoding='utf-8') as file:
    seoul_gu_dict = json.load(file)

initial_search_tags = [gu + "맛집" for gu in seoul_gu_dict.keys()]
# print(initial_search_tags)

# requesting crawl page
print(crawl_url + initial_search_tags[0] + "/으로 이동합니다.")
browser.get(crawl_url + initial_search_tags[0] + "/")
time.sleep(5) # waiting for page loading
browser.save_screenshot("C:/Users/minae2324/Documents/crawling_pic/search_page.png")


# post numbering variable & the number of further loading : total 600 posts
post_num = 0
total_loading_num = 3

# 저장할 리스트 생성
crawl_result_list = []

# ActionChains 인스턴스 생성 : action
action = ActionChains(browser)

# main crawling process
for i in range(total_loading_num):

    # check current status
    print("{}번째 posts 로딩".format(i+1))

    total_posts = browser.find_elements_by_class_name("_bz0w")
    total_posts_num = len(total_posts)

    print("{}개의 포스트가 있습니다.".format(total_posts_num))

    for j in range(total_posts_num)[post_num:total_posts_num]:
        # post 클릭, 대기

        total_posts[j].click()

        # (browser.find_element_by_xpath(
        #     "//*[@id='react-root']/section/main/article/div[1]/div/div/div[{}]/div[{}]/a".format(j//3+1, j%3+1))\
        #         .click())

        # (WebDriverWait(browser, 3)\
        #     .until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.RxpZH"))))
        time.sleep(3)
        browser.save_screenshot("C:/Users/minae2324/Documents/crawling_pic/click_post_{}.png".format(j+1))

        # 소스를 BS로 저장
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        # 이미지 url 추출
        img_url = soup.select_one("div._97aPb  div.KL4Bh > img")["src"]
        # print(img_url)

        # 위치명 및 ID 저장
        locations = soup.select_one("div.JF9hh > a")
        if locations:
            location_name, location_id = locations.text, locations["href"]
            # print(location_name, location_id)
        else:
            location_name = None
            location_id = None

        # 해시태그 저장
        post_hashtags = soup.select("div.EtaWk div.C4VMK > span > a")
        if post_hashtags:
            hashtags = [ht["href"] for ht in post_hashtags if ht is not None]
            # print(hashtags)

        # 좋아요 저장
        post_likes = soup.select_one("div.Nm9Fw > button > span")
        if post_likes is not None:
            likes = post_likes.text.replace(",", "")
        # print(likes)

        # 날짜 저장
        dates = soup.select_one("div.k_Q0X.NnvRN > a > time")["datetime"]
        # print(dates)

        # 추출한 내용들 dict로 저장
        result_dict = {
            'location_name' : location_name,
            'location_id' : location_id,
            'hash_tags' : hashtags,
            'likes' : likes,
            'dates' : dates,
            'img_url' : img_url
        }

        crawl_result_list.append(result_dict)

        # 포스트 페이지 나가기
        browser.find_element_by_css_selector("div.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button").click()
        time.sleep(3)

        # 마우스 이동
        action.move_to_element(total_posts[j])
        time.sleep(3)

        # soup 인스턴스 삭제
        del soup

    post_num = total_posts_num
    print("{}개의 포스트를 수집하였습니다.".format(post_num))


# quiting crawling
browser.close()

print(crawl_result_list)

# pandas dataframe 변환
crawl_result_df = pd.DataFrame(crawl_result_list)
print(crawl_result_df.head(20))


