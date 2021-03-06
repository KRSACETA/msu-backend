from json import JSONDecoder
import pytest

from msu import create_app, db, api
from msu.models import Admin, File, Post, Form

app = create_app(testing=True)

dec = JSONDecoder()
def decode(s):
    return dec.decode(s.decode())


@pytest.fixture
def client():
    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            db.session.add(Admin(
                username='user',
                password='pass',
                name='Bob',
            ))
            db.session.commit()
            yield c
            db.session.close()
            db.drop_all()


def login(client):
    return client.post('/login', data={
        'username': 'user',
        'password': 'pass',
    }, follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def insert_item(item):
    db.session.add(item)
    db.session.flush()
    return item


def test_posts_get(client):
    p = insert_item(Post(admin_id=1, subject='Title', body='Body'))

    rv = client.get('/api/posts')
    data = decode(rv.data)['data']

    assert rv.status_code == 200
    assert len(data) == 1
    assert data[0]['subject'] == 'Title'
    assert data[0]['body'] == 'Body'

    rv = client.get(f'/api/posts/{p.id}')
    data = decode(rv.data)['data']
    
    assert rv.status_code == 200
    assert data['subject'] == 'Title'
    assert data['body'] == 'Body'


def test_posts_post(client):
    rv = client.post('/api/posts', data={
        'subject': 'Hello World!',
        'body': 'A piece of text',
    })
    assert rv.status_code == 403

    login(client)

    rv = client.post('/api/posts', data={
        'subject': 'Hello World!',
        'body': 'A piece of text',
    })
    data = decode(rv.data)['data']
    assert rv.status_code == 201

    assert data['id']
    assert data['inserted_at']
    assert data['subject'] == 'Hello World!'
    assert data['body'] == 'A piece of text'

    p = Post.query.first()
    assert p.subject == 'Hello World!'
    assert p.body == 'A piece of text'


def test_posts_delete(client):
    p = insert_item(Post(admin_id=1, subject='Title', body='Body'))

    rv = client.delete(f'/api/posts/{p.id}')
    assert rv.status_code == 403
    assert Post.query.get(p.id) is not None

    login(client)
    rv = client.delete(f'/api/posts/{p.id}')
    assert rv.status_code == 204
    assert Post.query.get(p.id) is None


def test_forms_get(client):
    f1 = insert_item(Form(subject='Hello', body='I love you'))
    f2 = insert_item(Form(subject='Hi!', body='Thank you', private=True))
    f3 = insert_item(Form(subject='Hey', body="You're amazing", name='Bob'))

    rv = client.get('/api/forms')
    assert rv.status_code == 403

    login(client)
    rv = client.get('/api/forms')
    data = decode(rv.data)['data']
    assert rv.status_code == 200
    assert len(data) == 3

    rv = client.get('/api/forms?private=false')
    data = decode(rv.data)['data']
    assert rv.status_code == 200
    assert len(data) == 2

    rv = client.get('/api/forms?private=true')
    data = decode(rv.data)['data']
    assert rv.status_code == 200
    assert len(data) == 1

def test_forms_post(client):
    rv = client.post('/api/forms', json={
        'subject': 'Hello World!',
        'body': 'Your app is terrible',
    })

    assert rv.status_code == 201

    f = Form.query.first()
    assert f.subject == 'Hello World!'
    assert f.body == 'Your app is terrible'
    assert f.private == False
    assert f.name is None
