import datetime
import jwt
from flask import current_app
from tests.conftest import db


def test_메모장_저장(client):
    url = "https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=001&aid=0012407338"
    comment = 'test comment'

    data = {
        'url_give': url,
        'comment_give': comment
    }

    expiration_time = datetime.timedelta(hours=1)
    payload = {
        'id': 'tester',
        'exp': datetime.datetime.utcnow() + expiration_time
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET'])
    headers = {
        'authorization': f'Bearer {token}'
    }
    response = client.post('/memo', data=data, headers=headers)

    assert response.status_code == 200

    # mongodb 저장됐는지 확인
    memo = db.articles.find_one({'id': 'tester'}, {'_id': False})
    assert memo['comment'] == comment
