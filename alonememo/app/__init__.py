from flask import Flask
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = None


# 플라스크 프레임워크에서 지정한 함수 이름
# 플라스크 동작할 때, create_app() 함수 결과로 리턴한 앱 실행
def create_app(database_name='sparta'):
    # 플라스크 웹 서버 생성하기
    app = Flask(__name__)
    app.debug = True
    app.config.from_pyfile('config.py')

    global db
    db = client.get_database(database_name)

    # 순환 참조 방지
    from app.views import api, main, memo, user

    app.register_blueprint(api.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(memo.bp)
    app.register_blueprint(user.bp)

    return app
