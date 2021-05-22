from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup



# 플라스크 프레임워크에서 지정한 함수 이름
# 플라스크 동작시킬 때 create_app() 함수의 결과로 리턴한 앱을 실행시킨다
def create_app():
    # 플라스크 웹 서버 실행하기
    app = Flask(__name__)

    # mongodb 추가
    client = MongoClient('localhost', 27017)
    db = client.get_database('sparta')

    # API 추가
    @app.route('/', methods = ['GET'])  # 데코레이터 문법
    def index():  # 함수 이름은 고유해야 함
        memos = list(db.articles.find({}, {'_id': False}))
        return render_template('index.html', test = '테스트', memos=memos)

    # 로그인 화면
    @app.route('/login', methods=['GET'])
    def login():
        return render_template('login.html')

    # 가입 화면
    @app.route('/register', methods=['GET'])
    def register():
        return render_template('register.html')

    @app.route('/api/login', methods=['POST'])
    def api_login():
        id = requests.form['id_give']
        pw = requests.form['pw_give']

        # id, pw 검증 후에 JWT 만들어서 RETURN


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

    # 아티클 로드 API
    @app.route('/memo', methods=['GET'])
    def list_memo():
        memos = list(db.articles.find({}, {'_id': False}))
        return jsonify({
            'result': 'success',
            'articles': memos,
            'msg': '로드합니다.'}
        )

    return app


# app.py 파일 실행
# if __name__ == '__main__':
#     app.run(
#         '0.0.0.0',    # 모든 IP에서 오는 요청 허용
#         7000,         # 플라스크 웹 서버는 7000번 포트 사용
#         debug = True  # 에러 발생 시 에러 로그 보여줌
#     )

