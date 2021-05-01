import requests
import pprint

# HTTP GET request
response = requests.get(
    'http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99'
)
print(response)

result = response.json()
print(result)

pprint.pprint(result['RealtimeCityAir']['row'])

data = result['RealtimeCityAir']['row']

for datum in data:
    if datum['PM10'] < 20:
        print(datum['MSRSTE_NM'], datum['PM10'])