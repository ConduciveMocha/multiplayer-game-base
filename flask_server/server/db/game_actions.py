from sqlalchemy.orm.exc import NoResultFound

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


# test_tables()


def get_object_position(object_id):
    game_object = GameObject.query.filter_by(id=object_id).first()
    if game_object:
        return game_object.pos
    else:
        raise NoResultFound(f"Could not locate game object with id={object_id}")


def move_game_object(object_id, delta):
    game_object = GameObject.query.filter_by(id=object_id).first()
    if game_object:
        game_object.posx += delta.x
        game_object.posy += delta.y
        db.session.add(game_object)
        db.session.commit()
        return game_object
    else:
        raise NoResultFound(f"Could not locate game object with id={object_id}")


def test2():
    for a in GameObject.query.all():
        print(a.id)
