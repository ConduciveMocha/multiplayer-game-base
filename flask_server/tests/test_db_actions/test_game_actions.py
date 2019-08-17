import pytest
from server.game.geometric_types.vector import Vector
from server.db.models import GameObject
from server.db.game_actions import get_object_position

@pytest.fixture(scope='module')
def mock_game_objects(session):
    game_object_list = [GameObject(pos=Vector(0,0), dim=Vector(5,5))]
    for g in game_object_list:
        session.add(g)
    session.commit()
    yield game_object_list
    for g  in game_object_list:
        session.delete(g)
    session.commit()

def test_get_object_position(mock_game_objects):
    for g in mock_game_objects:
        assert g.pos == get_object_position(g.id)
