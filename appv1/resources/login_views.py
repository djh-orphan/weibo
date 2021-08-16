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
    def get(self):
        return make_response(render_template('login.html'))
    def post(self):
        parse.add_argument('signup',type=bool,location='json')
        args = parse.parse_args()
        # user = User.query.filter_by(username=args['username']).first()
        if not args['signup']:
            user = User.query_by_username(args['username'])
            if user is not None :
                if user.verify_pwd(args['pwd']):
                    login_user(user, True)
                    return make_response(marshal(user, user_field))
                else:
                    return "wrong pwd"
            else:
                return "Please SignUp"
        else:
           if User.adduser(args):
               return "注册成功，请登录"
           else:
               return "注册失败"

class UsersWithLogin(Resource):
    @login_required
    def post(self):
        args = parse.parse_args()
        if User.resetpwd(args):
            logout_user()
            return "重置成功，请重新登录"
        else:
            return "重置失败，请重试"

    @login_required
    def get(self):
        logout_user()
        return "登出成功"