from flask_restful import Resource, fields, marshal
from flask import render_template, redirect, url_for, make_response, session
from .parsers import parse
from flask_login import LoginManager, login_user, login_required, logout_user
from ..database.ormodels import User

login_manager = LoginManager()

user_field = {'username': fields.String,
              'email': fields.String,
              'id': fields.Integer,
              }


@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    return user


# class Login(Resource):
#     def get(self):
#         return make_response(render_template('login.html'))
#
#     def post(self):
#         args = parse.parse_args()
#         user = User.query_by_username(args['username'])
#         # user = User.query.filter_by(username=args['username']).first()
#         if user is not None and user.verify_pwd(args['pwd']):
#             login_user(user, True)
#             return make_response(marshal(user, user_field))
#
#
# class Resetpwd(Resource):
#     @login_required
#     def get(self):
#         return make_response(render_template('reset.html'))
#
#     @login_required
#     def post(self):
#         args = parse.parse_args()
#         if User.resetpwd(args):
#             logout_user()
#             return redirect(url_for('login.login'))
#         else:
#             return redirect(url_for('login.resetpwd'))
#
#
# class Signup(Resource):
#     def get(self):
#         return make_response(render_template('signup.html'))
#
#     def post(self):
#         args = parse.parse_args()
#         if User.adduser(args):
#             return redirect(url_for('login.login'))
#         else:
#             return redirect(url_for('login.signup'))
#
#
# class Logout(Resource):
#     @login_required
#     def get(self):
#         logout_user()
#         return redirect(url_for('login.login'))

class UsersWithoutLogin(Resource):

    def post(self):
        parse.add_argument('signup', type=bool, location='json')
        args = parse.parse_args()
        if not args['signup']:
            try:
                user = User.query_by_username(args['username'])
            except Exception as error:
                return {"work": False, "message": str(error.args)}
            else:
                if user is not None:
                    if user.verify_pwd(args['pwd']):
                        login_user(user, True)
                        rep = marshal(user, user_field, envelope="data")
                        rep["work"] = True
                        return rep
                    else:
                        return {"message": "wrong pwd", "work": False}
                else:
                    return {"message": "please signup", "work": False}
        else:
            try:
                res=User.adduser(args)
            except Exception as error:
                return {"message": str(error.args), "work": False}
            else:
                if res:
                    return {"message": "signup successful", "work": True}
                else:
                    return {"message": "user already exists", "work": False}


class UsersWithLogin(Resource):
    @login_required
    def post(self):
        args = parse.parse_args()
        try:
            res = User.resetpwd(args)
        except Exception as error:
            return {"message": str(error.args), "work": False}
        else:
            if res:
                logout_user()
                return {"message": "reset successful", "work": True}
            else:
                return {"message": "failed to reset", "work": False}

    @login_required
    def get(self):
        logout_user()
        return {"message": "logout successful", "work": True}
