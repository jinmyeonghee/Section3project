import re
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import requests
import csv
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd

# 제주 구 리스트
gu_list = ['한경면','한림읍','애월읍','우도면','조천읍','구좌읍','성산읍','표선면','남원읍','제주안덕면','대정읍']
list=[]
url = "https://map.kakao.com/"

options = webdriver.ChromeOptions()

options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
options.add_argument('lang=ko_KR')
chromdriver_path = "chromedriver"
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromdriver_path),
options=options)

driver.get(url)

searchloc = ("한림읍 카페")
filename = ("asdfasdf")

search_area = driver.find_element(By.XPATH, "//*[@id='search.keyword.query']")
search_area.send_keys(searchloc)  # 검색어 입력
driver.find_element(By.XPATH, "//*[@id='search.keyword.submit']").send_keys(Keys.ENTER)  
# Enter로 검색

time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="info.main.options"]/li[2]/a').send_keys(Keys.ENTER)
# 검색 후 장소 클릭
driver.implicitly_wait(5)

def CafeNamePrint():

    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    cafe_lists = soup.select('.placelist > .PlaceItem')
    count = 1
    
    for cafe in cafe_lists:
        temp=[]

        cafe_name = cafe.select('.head_item > .tit_name > .link_name')[0].text
        score = cafe.select('.rating > .score > .num')[0].text
        review = cafe.select('.rating > .review')[0].text
        link = cafe.select('.contact > .moreview')[0]['href']
        addr = cafe.select('.addr')[0].text

        temp.append(cafe_name)
        temp.append(score)
        temp.append(review)
        temp.append(link)
        temp.append(addr)
        driver.implicitly_wait(2)
        list.append(temp)
        

    f=open(filename+'.csv',"w",encoding="utf-8-sig", newline="")
    writercsv=csv.writer(f)
    header=['Name', 'Score', 'Review', 'Link', 'Addr']
    writercsv.writerow(header)

    for i in list:
        writercsv.writerow(i)

page = 1
page2 = 0
for i in range(0, 100000):
    try:
        page2+=1
        print("**", page, "**")
        driver.find_element(By.XPATH, f'//*[@id="info.search.page.no{page2}"]').send_keys(Keys.ENTER)
        CafeNamePrint()
        driver.implicitly_wait(3)
        if (page2)%5==0:
            driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
            page2=0
        page+=1
    except:
        break


print("**크롤링 완료**")

