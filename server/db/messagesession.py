from db.declaratives import User,PrivateMessage
from datetime import datetime
from db.dbsession import DBSession
class MessageSession(DBSession):


    def add_message(self,sender_id, reciever_id, content):
        with self.db_open():
            new_message = PrivateMessage(sender_id=sender_id,reciever_id=reciever_id,content=content,timestamp=datetime.utcnow())
            self.sess.add(new_message)
            self.sess.commit()
    def get_recent(self,user_id,from_user_id=None):
        pass