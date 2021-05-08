from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(
        '0.0.0.0',    # 모든 IP에서 오는 요청 허용
        7000,         # 플라스크 웹 서버는 7000번 포트 사용
        debug = True, # 에러 발생 시 에러 로그 보여줌
    )

