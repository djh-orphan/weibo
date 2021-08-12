from flask_login import UserMixin
from hashlib import md5

from .models import Userperson, db,Message


class User(UserMixin, Userperson):

    @staticmethod
    def query_by_username(username):
        return User.query.filter_by(username=username).first()

    def verify_pwd(self, pwd):
        hl = md5()
        hl.update((self.username + pwd).encode(encoding='utf-8'))
        if hl.hexdigest() == self.pwd:
            return True
        else:
            return False

    @staticmethod
    def get(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def adduser(args):
        username = args['username']
        email = args['email']
        hl = md5()
        hl.update((args['username'] + args['pwd']).encode(encoding='utf-8'))
        pwd = hl.hexdigest()
        if User.query_by_username(username) is  None:
            newUser = User(username=username, email=email, pwd=pwd)
            db.session.add(newUser)
            db.session.commit()
            return newUser
        else:
            return False

    @staticmethod
    def resetpwd(args):
        hl = md5()
        hl.update((args['username'] + args['pwd']).encode(encoding='utf-8'))
        pwd = hl.hexdigest()
        user=User.query_by_username(args['username'])
        if user is not None:
            user.pwd=pwd
            db.session.commit()
            return True
        else:
            return False

class Messages(Message):
    pass