def test_home_page_accessible(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Photos Galery" in response.data

def test_upload_requires_login_ui(client):
    response = client.get('/upload', follow_redirects=True)
    assert b"Login" in response.data or b"login" in response.data

def test_login_form_display(client):
    response = client.get('/login')
    assert b"User" in response.data
    assert b"Password" in response.data

def test_failed_login_feedback(client):
    response = client.post('/login', data={
        'username': 'wrong',
        'password': 'password'
    }, follow_redirects=True)
    assert b"Incorrect credentials" in response.data

def test_search_no_results(client):
    response = client.get('/?tag=nimportequoi')
    assert response.status_code == 200
    assert b"No photo found" in response.data