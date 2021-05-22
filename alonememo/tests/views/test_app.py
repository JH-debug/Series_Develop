import hashlib
import jwt
from tests.conftest import db


def test_register(client):
    data = {
        'id_give': 'tester01',
        'pw_give': 'test'
    }

    response = client.post('/api/register', data=data)

    assert response.status_code == 200


    user = db.users.find_one({'id': 'tester01'},
                             {'_id': False})

    # 패스워드 평문저장하지 않음
    user['pw'] != 'test'
    pw_hash = hashlib.sha256('test'.encode()).hexdigest()
    assert user['pw'] == pw_hash


def test_login(client):

    data = {
        'id_give': 'tester02',
        'pw_give': 'test'
    }

    # 먼저 회원가입
    client.post('/register', data=data)

    # 로그인
    response = client.post('/api/login', data=data)

    assert response.status_code == 200
    assert response.json['result'] == 'success'

    token = response.json['token']
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    assert payload['id'] == 'tester02'

