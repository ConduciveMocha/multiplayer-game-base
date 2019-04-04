from db.usersession import UserSession

sess = UserSession()

try:
    print(sess.add_user('nate12345678','password1234', 'email.3@email.coalm'))
except Exception as e:
    print(e)

try:
    print(sess.check_login('nate12345678','password1234'))
except Exception as e:
    print(e)

print(UserSession.valid_email('email3@email.com'))
print(UserSession.valid_email('asdf'))
