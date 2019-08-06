from server.redis_cache.poolmanager import global_poolman,global_pipe
from server.logging import make_logger



def create_user_lock(lockname, lock_duration):

    get_keyname = lambda id: f"{lockname}-{id}"

    #TODO add exception handling. Return false if lock was not set
    @global_poolman
    def set_lock(r,id):
        r.psetex(get_keyname(id),lock_duration,1)
        return True
    
    @global_poolman
    def check_locked(r,id):
        return r.exists(get_keyname(id))

    return set_lock,check_locked

set_move_lock,check_move_lock= create_user_lock('move-lock', 5)
set_message_lock,check_message_lock = create_user_lock('message-lock',100)
