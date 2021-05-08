# 포트 (컴퓨터 내 어떤 프로그램과 통신할 것인가)
# 0~65535번 포트까지 가능
# 0~1024는 국제표준, OS에서 사용
# mongodb는 기본으로 27017 포트

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# db 연결 확인
client = MongoClient('localhost', 27017)
db =  client.get_database('test')

'''
print(db)

db.person.insert_one(
    {'name': 'kim', 'age': 30}
)
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
response = requests.get(
    'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200716',
    headers = headers
)


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

        document = {
            'rank': int(rank_tag['alt']),
            'title': title_tag.text,
            'porint': float(grade_tag.text)
        }

        db.movies.insert_one(document)
        print('DB 적재 완료', document)

