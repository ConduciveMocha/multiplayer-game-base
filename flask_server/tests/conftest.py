import pytest

from app import create_app
from app import db as _db

from server.db.models import User,Email,Thread,Message, user_thread
from server.serverconfig import TestingConfig
from server.utils.data_generators import mock_user_list


def create_mock_users(db_session):
    
    user_list = []
    for u in mock_users_list():
        username, password, email = u
        try:
            current_user = User.query.filter_by(username=username, email=email).first()
            user_list.append(current_user)
        except Exception as e:
            try:
                new_user = User(username,password,email)
            except AssertionError:
                continue
            db_session.add(new_user)
            db_session.commit()
            user_list.append(new_user)
    # return user_list,mock_users


def populate_test_db(db_session)   :
    create_mock_users(db_session)    

@pytest.fixture(scope='session')
def mock_users(session):
    pass

# This fixes application context problem with 
# flask-sqlalchemy. Code came from:
# http://alexmic.net/flask-sqlalchemy-pytest/
@pytest.fixture(scope='session')
def app(request):
    app = create_app(TestingConfig)
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()
    request.addfinalizer(teardown)
    return app

@pytest.fixture(scope='session')
def db(app,request):


    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    connection = _db.engine.connect()
    transaction= connection.begin()
    options=dict(bind=connection,binds={})
    session = _db.create_scoped_session(options=options)
    db.session = session
    
    populate_test_db(session)

    transaction.rollback()
    connection.close()
    session.remove()
    

    request.addfinalizer(teardown)
    return _db

@pytest.fixture(scope='function')
def session(db,request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

@pytest.fixture
def client(app):
    client = app.test_client()
    return client





