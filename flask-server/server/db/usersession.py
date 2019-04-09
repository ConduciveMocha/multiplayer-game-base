import re
import logging
from contextlib import contextmanager
from werkzeug.security import generate_password_hash, check_password_hash

from server.db.declaratives import User, Email
from server.db.dbsession import DBSession
class UserSession(DBSession):    
    # Validation Functions
    @staticmethod
    def valid_email(email):
        fm =  re.fullmatch(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}$', email,flags=re.IGNORECASE)
        return True if fm else False
    
    @staticmethod
    def valid_username(username):
        if re.fullmatch(r'^[0-9_]{8,16}$',username):
            return False
        fm = re.fullmatch(r'^[A-Za-z0-9_]{8,16}$',username)
        return True if fm else False

    @staticmethod
    def valid_password(password):
        fm = re.fullmatch(r'^\S{8,16}$',password)
        return True if fm else False
    
    # Checks if username has been registered; Returns boolean
    def username_in_use(self,username):
        with self.db_open():
            result = self.session.query(User.username).filter(User.username==username).one_or_none()
        return result is not None

    # Checks if email has been registered; returns boolean
    def email_in_use(self,email):
        with self.db_open():
            result = self.session.query(Email.email).filter(Email.email==email).one_or_none()
        return result is not None

    # Checks if all fields are valid
    def validate_info(self,username,password,email):
        if not UserSession.valid_username(username):
            return 'invalid username'
        if not UserSession.valid_password(password):
            return 'password incorrect length' 
        if not UserSession.valid_email(email):
            return 'invalid email'
        if self.username_in_use(username):
            return 'username in use'
        if self.email_in_use(email):
            return 'email in use'    
        return None

        
    def add_user(self, username,password,email):
        with self.db_open():
            logging.info('MYSQL: ADDING USER')
            validation_error = self.validate_info(username,password,email)
            if validation_error: return validation_error,-1
            
            method, password_salt, password_hash = generate_password_hash(password).split('$')

            new_user = User(username=username,password_hash=password_hash,password_salt=password_salt)
            self.session.add(new_user)
            self.session.commit()
            new_email = Email(email=email, verified=False, user_id=new_user.id)
            self.session.add(new_email)
            self.session.commit()
            return 'success',new_user.id
        
    def check_login(self,username,password):
        with self.db_open():
            result= self.session.query(User.id,User.password_hash,User.password_salt).filter(User.username == username).one_or_none()
            if not result:
                return 'account not found'
            user_id,password_hash,password_salt = result
            hash_string = '$'.join(
                ['pbkdf2:sha256:50000', password_salt, password_hash])
            


            if check_password_hash(hash_string,password):
                return user_id
            else:
                return 'username or password are incorrect'


