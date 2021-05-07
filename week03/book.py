import pprint
import requests
import secret

# HTTP GET request
response = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
# json 파일로 가져옴
result = response.json()
data = result['RealtimeCityAir']['row']

for datum in data:
    state = datum['MSRSTE_NM']
    pm10 = datum['PM10']
    if pm10 > 25:
        # fstring
        print(f'{state} - {pm10}')

book_name = '프리워커스'
naver_url = f'https://openapi.naver.com/v1/search/book.json?query={book_name}'

headers = {
    'X-Naver-Client-Id': secret.client_id,
    'X-Naver-Client-Secret': secret.client_secret
}

response = requests.get(naver_url, headers=headers)
pprint.pprint(response.json())