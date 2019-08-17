import pytest
from server.game.geometric_types.vector import Vector
from server.db.models import GameObject
from server.db.game_actions import get_object_position,move_game_object

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

def test_move_game_object(mock_game_objects):
    delta = Vector(10,5)
    for  g in mock_game_objects:
        original_pos = g.pos
        assert g.pos + delta == move_game_object(g.id,delta)
# TODO Write test
def test_move_game_object_with_detection(mock_game_objects):
    assert True

def 