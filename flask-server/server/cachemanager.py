import logging

import redis

class CacheManager:
    def __init__(self):
        self.r = redis.Redis(host='localhost',port=6379)
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        
        self.create_user_hash()

    def create_user_hash(self):
        self.log.debug('create_user_hash called')
        
        if self.r.exists('users'):
            self.log.debug('Hash \'users\' exists. Returning.')
            return False

        else:
            self.r.hset('users', 0, 'SERVER')
            self.log.info("Hash 'users' has been created")
            return True


    def add_user(self,user_id,username):
        self.log.debug('add_user called')

        if self.r.hget('users', user_id):
            self.log.info('User %s already in users', user_id)
            return False
        elif self.r.hexists(username):
            self.log.warning('User %s found with incorrect user_id', username)
            return False
        else:
            self.r.hset('users',user_id,username)
            return True
    
    def remove_user(self,user_id):
        self.log.debug('remove_user called')
        if self.r.hget('users', user_id):
            self.r.hdel(user_id)
            self.log.info('User %s has been removed from users hash', user_id)
            return True
        else:
            self.log.info('User %s was not found in users hash',user_id)
            return False


    #TODO Finish up
    def create_message_thread(self,thread_id,members):
        self.log.debug('create_message_thread called')
        if self.r.exists(f'thread:{thread_id}'):
            self.log.info('Thread %s exists. Retrieving Message history', thread_id)
            return self.thread_history(thread_id)
        else:
            self.r.hmset(f'thread:{thread_id}', {})
            
    def thread_history(self,thread_id, nMessages=25):
        pass
    
CacheManager().create_user_hash()