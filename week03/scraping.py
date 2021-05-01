# https://velog.io/@c_hyun403/Python-WEB-CRAWLING
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
response = requests.get(
    'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200716',
    headers = headers
)

# print(response.text)

soup = BeautifulSoup(
    response.text, 'html.parser'
)

selector = '#old_content > table > tbody > tr'
title_selector = 'td.title > div > a'
rank_selector = 'td.ac > img'
grade_selector = 'td.point'

titles = soup.select(selector)
for title in titles:
    title_tag = title.select_one(title_selector)
    rank_tag = title.select_one(rank_selector)
    grade_tag = title.select_one(grade_selector)
    if title_tag:
        print(rank_tag['alt'], title_tag.text, grade_tag.text)

