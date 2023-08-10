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
gu_list = ['우도면','한경면','한림읍','애월읍','조천읍','구좌읍','성산읍','표선면','남원읍','제주안덕면','대정읍']
list=[]
url = "https://map.kakao.com/"

options = webdriver.ChromeOptions()

options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
options.add_argument('lang=ko_KR')
chromdriver_path = "chromedriver"
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromdriver_path),
options=options)

driver.get(url)

for gu in gu_list:
    def gu_search(gu):
        search_area = driver.find_element(By.XPATH, "//*[@id='search.keyword.query']")
        search_area.clear()
        search_area.send_keys(gu + "카페")  # 검색어 입력
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
        

            f=open(gu+'.csv',"w",encoding="utf-8-sig", newline="")
            writercsv=csv.writer(f)
            header=['Name', 'Score', 'Review', 'Link', 'Addr']
            writercsv.writerow(header)

            for i in list:
                writercsv.writerow(i)

        page = 1
        page2 = 0
        for i in range(0, 35):
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

    gu_search(gu)


# 행정구역카페 csv파일들 병합
path = './'
forders = os.listdir(path) #프로젝트3 디렉토리
df_all = pd.DataFrame()
for i in range(0,len(forders)):
    if forders[i].split('.')[1] == 'csv':
        file = forders[i]
        df= pd.read_csv(file,encoding='utf-8') 
        df_all = pd.concat([df_all, df])

df_all.to_csv("jejuallcafe.csv", encoding = "utf-8-sig")


# 데이터 정제시작 #
# 1. 데이터 전처리
df = pd.read_csv('jejuallcafe.csv', encoding='utf-8')

dfl = df.drop_duplicates(subset='Link')
dfln = dfl.drop_duplicates(subset='Name')
# print(dfln.isnull().sum())
# 결측치 score에만 존재
cafe = dfln.fillna(dfln['Score'].mean())
cafe = cafe[cafe['Addr'].str.contains('제주특별자치도')]

hangyeong = cafe[cafe['Addr'].str.contains('한경면')]
hangyeong = pd.DataFrame(hangyeong)
hangyeong['area'] = 'hangyeong'
hanlim = cafe[cafe['Addr'].str.contains('한림읍')]
hanlim = pd.DataFrame(hanlim)
hanlim['area'] = 'hanlim'
andeok = cafe[cafe['Addr'].str.contains('안덕면')]
andeok = pd.DataFrame(andeok)
andeok['area'] = 'andeok'
pyoseon = cafe[cafe['Addr'].str.contains('표선면')]
pyoseon = pd.DataFrame(pyoseon)
pyoseon['area'] = 'pyoseon'
udo = cafe[cafe['Addr'].str.contains('우도면')]
udo = pd.DataFrame(udo)
udo['area'] = 'udo'
daejeong = cafe[cafe['Addr'].str.contains('대정읍')]
daejeong = pd.DataFrame(daejeong)
daejeong['area'] = 'daejeong'
namwon = cafe[cafe['Addr'].str.contains('남원읍')]
namwon = pd.DataFrame(namwon)
namwon['area'] = 'namwon'
sungsan = cafe[cafe['Addr'].str.contains('성산읍')]
sungsan = pd.DataFrame(sungsan)
sungsan['area'] = 'sungsan'
gujwa = cafe[cafe['Addr'].str.contains('구좌읍')]
gujwa = pd.DataFrame(gujwa)
gujwa['area'] = 'gujwa'
jochen = cafe[cafe['Addr'].str.contains('조천읍')]
jochen = pd.DataFrame(jochen)
jochen['area'] = 'jochen'
aewol = cafe[cafe['Addr'].str.contains('애월읍')]
aewol = pd.DataFrame(aewol)
aewol['area'] = 'aewol'

jejuarea = pd.concat([hangyeong, hanlim, andeok, pyoseon, udo, daejeong, namwon, sungsan, gujwa, jochen, aewol])
jejuarea['Review'] = jejuarea['Review'].str.replace('리뷰', '')
jejuarea = jejuarea.reset_index(drop=True)
jejuarea['Review'] = jejuarea['Review'].str.replace(',', '')
jejuarea['Review'] = jejuarea['Review'].astype(int)
jejuarea['Score'] = round(jejuarea['Score'], 2)



# 2. 위도 경도 추가
import googlemaps
gmaps_key = "AIzaSyAvpG2I3R-WWtkHHwXTQvpmy8Uduy1iRtk"
gmaps = googlemaps.Client(key = gmaps_key)
lat = []
lng = []

for addr in jejuarea['Addr']:
    tmpmap = gmaps.geocode(addr, language='ko')
    if tmpmap:
        tmploc = tmpmap[0].get('geometry')
        lat.append(tmploc['location']['lat'])
        lng.append(tmploc['location']['lng'])
    else:
        lat.append("0")
        lng.append("0")

print("추가완료")

jejuarea['lat'] = lat
jejuarea['lng'] = lng

jejuarea = jejuarea.query("lat != '0'")
print(jejuarea.columns)
jejuarea = jejuarea.iloc[:,1:]
print(jejuarea.columns)
jejuarea.to_csv('jejulatlng.csv', encoding = "utf-8-sig")
# DB인서트
import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="jejucafe",
    user="postgres",
    password="1234")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS JEJUCAFE;")
cur.execute('''CREATE TABLE jejudocafe(
                cafe_id serial PRIMARY KEY,
                name VARCHAR(50),
                score FLOAT4,
                review INT,
                link VARCHAR(50),
                addr VARCHAR(128),
                area VARCHAR(50),
                lat FLOAT4,
                lng FLOAT4);''')

sql = "INSERT INTO jejudocafe (cafe_id, name, score, review, link, addr, area, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
with open('jejulatlng.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        cur.execute(sql,row)

conn.commit()