from db.db import Session
from db.messagesession import MessageSession
from db.usersession import UserSession
from db.declaratives import User
# try:
#     user_sess = UserSession()
#     user_sess.add_user('nate12345678','password1234','email.email@email.com',dob=None)
#     user_sess.add_user('paul12345678','password1234','email.email@gmail.com',dob=None)
#     print('created_users')
#     message_sess = MessageSession()
#     message_sess.add_message(1,2,"content")
#     sess = Session()
#     for resp in sess.query(User).order_by(User.id):
#         for m in resp.sent_messages:
#             print(m)

# except Exception as e:
#     print(e)
