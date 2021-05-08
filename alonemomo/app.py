from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# mongodb 추가
client = MongoClient('localhost', 27017)
db = client.get_database('sparta')

# API 추가
@app.route('/', methods = ['GET'])  # 데코레이터 문법
def index():  # 함수 이름은 고유해야 함
    return render_template('index.html', test = '테스트')


# 아티클 추가 API
@app.route('/memo', methods = ['POST'])
def save_memo():
    form = request.form
    url_receive = form['url_give']
    comment_receive = form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    response = requests.get(
        url_receive,
        headers=headers
    )

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')
    url = soup.select_one('meta[property="og:url"]')
    image = soup.select_one('meta[property="og:image"]')
    description = soup.select_one('meta[property="og:description"]')
    print(title['content'])
    print(url['content'])
    print(image['content'])
    print(description['content'])

    document = {
        'title': title['content'],
        'url': url['content'],
        'image': image['content'],
        'description': description['content'],
        'comment': comment_receive
    }

    db.articles.insert_one(document)
    return jsonify(
        {'result': 'success', 'msg': '저장됐습니다.'}
    )

@app.route('/memo', methods=['GET'])
def list_memo():
    memos = list(db.articles.find({}, {'_id': False}))
    return jsonify({
        'result': 'success',
        'articles': memos}
    )

# app.py 파일 실행
if __name__ == '__main__':
    app.run(
        '0.0.0.0',    # 모든 IP에서 오는 요청 허용
        7000,         # 플라스크 웹 서버는 7000번 포트 사용
        debug = True  # 에러 발생 시 에러 로그 보여줌
    )

