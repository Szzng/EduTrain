import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edu.settings")
import django
django.setup()

from pathlib import Path
from myfunc import *
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
from course.models import *

tcv_url = "http://www.teacherville.co.kr/trainapply/allCourseList.edu"
bws = get_selenium_bws(tcv_url)

# 화면 가장 아래로 스크롤 계속 내리기
interval = 3
prev_height = bws.execute_script("return document.body.scrollHeight")
while True:
    bws.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(interval)
    curr_height = bws.execute_script("return document.body.scrollHeight")

    if curr_height == prev_height:
        try:
            btn_more = bws.find_element(By.XPATH, '//*[@id="more"]/div/button')
            bws.execute_script("arguments[0].click();", btn_more)
        except:
            break
    else:
        prev_height = curr_height

# Get Data
columns = ['category', 'title', 'credit', 'price', 'summary', 'contents', 'link', 'img_idx']
tcv_df = pd.DataFrame(columns=columns)

soup = bs(bws.page_source, "lxml")
courses = soup.find_all('div', class_="info-box")

for idx, course in enumerate(courses):
    if len(course) <= 1: continue

    img_url = course.find('div', class_="photo-item").find('img')['src']
    image_res = requests.get(img_url)
    image_res.raise_for_status()
    img_path = os.path.join(Path(__file__).resolve().parent.parent, 'static_storage', 'img', 'tcv', f'{idx}.jpg')
    with open(img_path, "wb") as f:
        f.write(image_res.content)

    infos = course.find('div', class_="title").find_all('span')
    credit = infos[0].get_text().strip()
    category = infos[1].get_text().strip()
    title = course.find('p', class_="text").get_text().strip()
    price = course.find('div', class_="cost-group").find_all('span')[0].get_text().strip()[:-1]
    pre_link = course.find('button', class_="training-btn blue")['onclick'].split('(')[1].split("'")
    seq = pre_link[1]
    dvs = pre_link[3]
    link = f'http://www.teacherville.co.kr/trainapply/courseDetail.edu?division={dvs}&courseSeq={seq}'
    detail_bws = get_selenium_bws(link)
    detail_bws.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    detail_soup = bs(detail_bws.page_source, "lxml")
    try:
        # summary = detail_soup.find('div', class_="info-txt-box").find_all('li')[1].find_all('p')[-1].get_text().strip()
        pre_summary = detail_soup.find('div', class_="info-txt-box").find_all('li')
        summary = []
        for s in pre_summary:
            summary.append(s.get_text().strip())
    except:
        print(link)
        summary = ''
    contents = []
    pre_contents = detail_soup.find('ul', id="contentsList").find_all('li')
    for content in pre_contents:
        contents.append(content.get_text().strip())
    tcv_df.loc[len(tcv_df)] = [category, title, credit, price, summary, contents, link, idx]

bws.quit()
print(tcv_df)

# Clean the Data
tcv_df['price'] = tcv_df['price'].apply(lambda x: x.replace(',', '')).astype(int)
tcv_df['site'] = 'tcv'

# manage DB
Course.objects.all().delete()

for category in tcv_df['category'].drop_duplicates().values:
    Category(name=category).save()

for t in tcv_df.itertuples():
    Course(
        category_id=t.category, title=t.title, credit=t.credit,
        price=t.price, summary=t.summary, contents=t.contents,
        link=t.link, site=t.site, img_idx=t.img_idx
    ).save()


