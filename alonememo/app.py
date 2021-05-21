import datetime
import hashlib
import os
import jwt as jwt
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

# mongodb 추가
client = MongoClient('localhost', 27017)
db = client.get_database('sparta')

# .env 파일로 환경변수로 설정
load_dotenv()
# 환경변수 읽어오기
JWT_SECRET = os.environ['JWT_SECRET']
CLIENT_ID = os.environ['CLIENT_ID']
CALLBACK_URL = os.environ['CALLBACK_URL']
SERVICE_URL = os.environ['SERVICE_URL']


# API 추가
@app.route('/', methods = ['GET'])  # 데코레이터 문법
def index():  # 함수 이름은 고유해야 함
    # 파이썬 .get() 함수는 딕셔너리에서 값이 없을 경우, 에러가 나는 대신, None을 가져옴
    token = request.cookies.get('loginToken')
    
    # 메모 리스트 불러올 때 로그인 id 정보로 필터링
    if token:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            print(payload)
            memos = list(db.articles.find({'id': payload['id']}, {'_id': False}))
        except jwt.ExpiredSignatureError:
            memos = {}

    else:
        memos = {}

    return render_template('index.html', test = '테스트', memos=memos)


# 로그인 화면
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html',
                            CLIENT_ID=CLIENT_ID,
                            CALLBACK_URL=CALLBACK_URL,
                            SERVICE_URL=SERVICE_URL)


# 로그인 API
@app.route('/api/login', methods=['POST'])
def api_login():
    id = request.form['id_give']
    pw = request.form['pw_give']

    # id, pw 검증 후에 JWT 만들어서 return
    pw_hash = hashlib.sha256(pw.encode()).hexdigest()
    user = db.users.find_one({'id': id, 'pw': pw_hash}, {'_id': False})

    # 가입 상태
    if user:
        # jwt가 1시간 동안 유효
        expiration_time = datetime.timedelta(hours=1)
        # 현재 시간 + 1
        payload = {
            'id': id,
            'exp': datetime.datetime.utcnow() + expiration_time
        }
        # 코드로 관리해서는 안되는 비밀값은 아래와 같이 처리
        token = jwt.encode(payload, JWT_SECRET)
        print(token)
        return jsonify({'result': 'success', 'token': token})

    # 가입하지 않은 상태
    else:
        return jsonify({'result': 'fail', 'msg': '로그인 실패'})


# 회원가입 화면
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


# 회원가입 API
@app.route('/api/register', methods=['POST'])
def api_register():
    id = request.form['id_give']
    pw = request.form['pw_give']

    user = db.users.find_one({'id': id}, {'_id': False})

    if id.strip() or pw.strip() == '':
        return jsonify({'result': 'fail', 'msg': '아이디와 비밀번호를 모두 입력해주세요.'})

    elif id == user['id']:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디가 있습니다. 아이디를 다시 설정해주세요.'})

    else:
        # 회원가입

        # hash
        # 1. 일정한 크기의 암호문으로 변경 (자릿수 노출 방지)
        # 2. 복원 불가 (db에는 hash된 값 저장, 해시된 값을 비교
        # 나라에서 hash 방식을 정해놓음
        # sha256을 많이 씀
        # hexdigest(): hash하면 사람이 읽을 수 없음, 따라서 문자열로 바꿔줌

        # salting
        # 1. pw + 랜덤 문자열 추가(솔트)
        # 2. 솔트 추가된 비밀번호를 해시
        # db에 저장할 때는 (해시 결과물 + 적용한 솔트) 묶어서 저장

        pw_hash = hashlib.sha256(pw.encode()).hexdigest()
        db.users.insert_one({'id': id, 'pw': pw_hash})

        return jsonify({'result': 'success'})


# 네이버 로그인 화면
@app.route('/naver', methods=['GET'])
def callback():
    return render_template('callback.html',
                           CLIENT_ID=CLIENT_ID,
                           CALLBACK_URL=CALLBACK_URL)

# 네이버로 로그인 API
@app.route('/api/register/naver', methods=['POST'])
def api_register_naver():
    naver_id = request.form['naver_id']

    if not db.users.find_one({'id': naver_id}, {'_id': False}):
        db.users.insert_one({'id': naver_id, 'pw': ''})

    # JWT 발급
    expiration_time = datetime.timedelta(hours=1)

    payload = {
        'id': naver_id,
        'exp': datetime.datetime.utcnow() + expiration_time
    }

    token = jwt.encode(payload, JWT_SECRET)
    print(token)
    return jsonify({'result': 'success', 'token': token})


# JWT 생성
@app.route('/user', methods=['POST'])
def user_info():
    token_receive = request.headers['authorization']
    token = token_receive.split()[1]
    print(token)

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        print(payload)
        return jsonify({'result': 'success', 'id': payload['id']})

    except jwt.exceptions.ExpiredSignatureError:
        # try 부분을 실행했지만 위와 같은 에러가 난다면 (이 에러는 유효 시간이 지났을 때 발생)
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})


# 아티클 추가 API
@app.route('/memo', methods = ['POST'])
def save_memo():
    form = request.form
    url_receive = form['url_give']
    comment_receive = form['comment_give']

    # JWT 추출
    token_receive = request.headers['authorization']
    token = token_receive.split()[1]
    print(token)

    try:
        # JWT 페이로드에서 id 확인
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        id = payload['id']

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
            'comment': comment_receive,
            'id': id
        }

        db.articles.insert_one(document)
        return jsonify(
            {'result': 'success', 'msg': '저장됐습니다.'}
        )
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})


# 아티클 로드 API
@app.route('/memo', methods=['GET'])
def list_memo():
    memos = list(db.articles.find({}, {'_id': False}))
    return jsonify({
        'result': 'success',
        'articles': memos,
        'msg': '로드합니다.'}
    )


# app.py 파일 실행
if __name__ == '__main__':
    app.run(
        '0.0.0.0',    # 모든 IP에서 오는 요청 허용
        7000,         # 플라스크 웹 서버는 7000번 포트 사용
        debug = True  # 에러 발생 시 에러 로그 보여줌
    )

