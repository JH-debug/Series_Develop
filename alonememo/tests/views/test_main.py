# test 함수는
# test_ 접두사로 시작
# client 인자는 웹브라우져 클라이언트처럼 동작
# client 인자 설정은 pytest-flask 패키지에서 작업해줌
def test_main_page(client):
    print('test')
    response = client.get('/')

    # assert 조건을 만족하는 것이 테스트 통과 조건
    assert response.status_code == 200


def test_login_page(client):
    print('test')
    response = client.get('/login')

    assert response.status_code == 200


def test_register_page(client):
    print('test')
    response = client.get('/register')

    assert response.status_code == 200


def test_invalid_page(client):
    print('test')
    response = client.get('/invalid')

    assert response.status_code == 404