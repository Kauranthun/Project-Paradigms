from app.models.models import User, Photo, db

def test_user_creation_integration(client):
    user = User(username="testuser", password="hashedpassword", package="FREE")
    db.session.add(user)
    db.session.commit()
    assert User.query.filter_by(username="testuser").first() is not None

def test_photo_link_to_user(client):
    user = User(username="owner", password="pw")
    db.session.add(user)
    db.session.commit()
    photo = Photo(filename="img.jpg", user_id=user.id)
    db.session.add(photo)
    db.session.commit()
    assert len(user.photos) == 1

def test_search_by_hashtag_logic(client):
    p = Photo(filename="1.jpg", hashtags="#nature", user_id=1)
    db.session.add(p)
    db.session.commit()
    results = Photo.query.filter(Photo.hashtags.contains("nature")).all()
    assert len(results) == 1

def test_delete_user_cascade(client):
    user = User(username="del", password="pw")
    db.session.add(user)
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    assert db.session.get(User, user.id) is None

def test_download_non_existent_photo(client):
    response = client.get('/download/999')
    assert response.status_code == 404