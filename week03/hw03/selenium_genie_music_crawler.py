from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import secret

url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20210501'

chromedriver = secret.chrome_driver
driver = webdriver.Chrome(chromedriver)
driver.get(url)

search_box = driver.find_element_by_xpath('//*[@id="sc-fd"]')
search_box.send_keys('브레이브걸스')
search_box.send_keys(Keys.RETURN)

soup = BeautifulSoup(
    driver.page_source, 'html.parser'
)

selector = '#body-content > div > div > div > table > tbody > tr'
list_ = soup.select(selector)

for music in list_:
    title = music.select_one('td.info > a.title.ellipsis').text.strip()
    album = music.select_one('td.info > a.albumtitle.ellipsis').text.strip()
    print(title, album)

driver.close()

