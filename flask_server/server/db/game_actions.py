from sqlalchemy.orm.exc import NoResultFound

from app import db
from server.db.models import GameObject, Environment, User,UserInventory
from server.logging import make_logger
from server.game.geometric_types.vector import Vector

logger = make_logger(__name__)


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
    logger.info(f'Getting position of object with id={object_id}')
    game_object = GameObject.query.filter_by(id=object_id).first()
    if game_object:
        logger.info(f'Found object with id={object_id}. Position={game_object.pos}')
        return game_object.pos
    else:
        logger.error(f"Could not locate game object with id={object_id}")
        raise NoResultFound(f"Could not locate game object with id={object_id}")


def move_game_object(object_id, delta, collision_function=None):
    game_object = GameObject.query.filter_by(id=object_id).first()
    if game_object:
        if collision_function and collision_function(game_object,delta):
           logger.info('Player object not moved')
           return game_object
        else:
            game_object.pos += delta
            db.session.add(game_object)
            db.session.commit()
            return game_object
    else:
        raise NoResultFound(f"Could not locate game object with id={object_id}")

def check_user_owns_object(user_id,game_object_id):
    game_object = GameObject.query.filter_by(id=game_object_id)
    return user_id == game_object.owner_id
        
def object_in_inventory(inventory_object_id, user_id):
    try:
        ui = UserInventory.query.filter_by(user_id=user_id, inventory_object_id=inventory_object_id).one()
        return ui.quantity > 0
    except AttributeError:
        return False
    except NoResultFound:
        return False

def object_in_enviroment(env_id, game_object_id):
    env_game_objects = Environment.query.filter_by(id=env_id).one().game_objects
    return game_object_id in map(lambda game_object: game_object.id, env_game_objects)
# TODO Fix exception types in boundary check
def switch_environments(game_object_id,env_id, pos=Vector(0,0)):
    new_env  = Environment.query.filter_by(id=env_id)
    game_object = GameObject.query.filter_by(id=game_object_id)
    if not new_env:
        raise NoResultFound(f'No environment found with id={env_id}')
    elif not game_object:
        raise NoResultFound(f'No GameObject found with id={game_object_id}')
    # Boundary Check
    if pos.x + game_object.width > new_env.width:
        raise ValueError('HEYCHANGETHISEXCEPIONTYPE\nGameObject out of bounds (x)')
    elif pos.y + game_object.height > new_env.height:
        raise ValueError('HEYCHANGETHISEXCEPIONTYPE\nGameObject out of bounds (y)')
    # Everything peachy. Set position
    else:
        game_object.environment = new_env
        game_object.pos = pos
    
# def pickup_item(user_id, game_object_id):
#     game
        


def add_to_user_inventory(inv_obj_id, user_id,quantity=1):
    user_inv = UserInventory.query.filter_by(user_id=user_id, inventory_object_id=inv_obj_id).first()

    if user_inv is None:
        user_inv = UserInventory(quantity=quantity, user_id=user_id, inventory_object_id=inv_obj_id)
        
    else:
        user_inv.quantity += quantity
        
    db.session.add(user_inv)
    db.session.commit()

def get_user_inventory(user_id):
    logger.info(f'Getting user inventory for user with id={user_id}')
    if User.query.filter_by(id=user_id).one():
        return UserInventory.query.filter_by(user_id=user_id)
    else:
        logger.error(f'No result found for user with id={user_id}')
        raise NoResultFound(f'User with id={user_id} does not exist.')

def 


# TODO Find better exception to throw than DataError.
def remove_from_user_inventory(inv_obj_id,user_id,quantity=1, raise_underflow_error=False):
    user_inv = UserInventory.query.filter_by(user_id=user_id, inventory_object_id=inv_obj_id).first()
    if user_inv is None:
        logger.error(f'User does not have object with id={inv_obj_id} in inventory.')
        if raise_underflow_error:
            raise DataError('User does not have object')
    else:
        if user_inv < quantity:
            if raise_underflow_error:
                logger.error(f'User (id={user_id}) underflowed item (id={inv_obj_id}). Quantity in inventory= {user_inv.quantity}. Requested removal quantity={quantity}')
                raise DataError('Underflowed inventory quantity')
            else:
                user_inv.quantity = 0
                db.session.add(user_inv)
                db.session.commit()
        else:
            user_inv.quantity -= quantity
            db.session.add(user_inv)
            db.session.commit() 

def test2():
    for a in GameObject.query.all():
        print(a.id)
