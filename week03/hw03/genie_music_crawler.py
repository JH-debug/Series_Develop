import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20210501'
response = requests.get(
    url,
    headers = headers
)

soup = BeautifulSoup(
    response.text, 'html.parser'
)

selector = '#body-content > div > div > table > tbody > tr'
title_selector = 'td.info > a.title.ellipsis'
rank_selector = 'td.number'
artist_selector = 'td.info > a.artist.ellipsis'

list_ = soup.select(selector)
for music in list_:
    title = music.select_one(title_selector).text.strip()
    rank = music.select_one(rank_selector).text[0:2].strip()
    artist = music.select_one(artist_selector).text.strip()
    print(rank, title, artist)
