from flask import Flask, render_template

app = Flask(__name__)


# API 추가
@app.route('/', methods = ['GET'])  # 데코레이터 문법
def index():  # 함수 이름은 고유해야 함
    return render_template('index.html', test = '테스트')

# app.py 파일 실행
if __name__ == '__main__':
    app.run(
        '0.0.0.0',    # 모든 IP에서 오는 요청 허용
        7000,         # 플라스크 웹 서버는 7000번 포트 사용
        debug = True  # 에러 발생 시 에러 로그 보여줌
    )

