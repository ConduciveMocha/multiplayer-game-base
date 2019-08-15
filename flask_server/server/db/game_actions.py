from app import db
from server.db.models import GameObject, Environment, User
from server.logging import make_logger


def test_tables():
    new_env = Environment(width=20, height=50)
    new_go = GameObject(
        width=5,
        height=5,
        posx=0,
        posy=0,
        acquirable=True,
        collidable=False,
        environment=new_env,
    )
    db.session.add(new_env)
    db.session.add(new_go)
    db.session.commit()


test_tables()


def test2():
    for a in GameObject.query.all():
        print(a.id)
