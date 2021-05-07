# 참고: https://wikidocs.net/44095
import requests
import secret
import pprint

text = "안녕하세요"
data = "source=ko&target=en&text=" + text
naver_url = 'https://openapi.naver.com/v1/papago/n2mt'

headers = {
    'X-Naver-Client-Id': secret.client_id,
    'X-Naver-Client-Secret': secret.client_secret
}

data = {'source':'ko',
        'target':'en',
        'text': text.encode('utf-8')}

response = requests.post(naver_url,
                        headers = headers,
                        data = data)

print(response)
pprint.pprint(response.json())

result = response.json()
print(result['message']['result']['translatedText'])
