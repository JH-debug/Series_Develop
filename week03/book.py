import requests
import secret

book_name = '인공지능'
naver_url = 'https://openapi.naver.com/v1/search/book.xml?query=' + book_name + '&display=1&start=1'

headers = {
    'X-Naver-Client-Id': secret.client_id,
    'X-Naver-Client-Secret': secret.client_secret
}

response = requests.get(naver_url,
                        headers = headers)

print(response)