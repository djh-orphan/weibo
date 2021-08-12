from flask import Blueprint, url_for
from flask_restful import Api
from .login_views import UsersWithLogin,UsersWithoutLogin
from .weibo_views import Weibos, Comments, Top10

user=Blueprint("user", __name__)

api=Api(user)
# api.add_resource(Login,'/login/')
# api.add_resource(Logout,'/logout/')
# api.add_resource(Signup,'/signup/')
# api.add_resource(Resetpwd, '/reset/')
api.add_resource(UsersWithoutLogin,'/login/','/signup/')
api.add_resource(UsersWithLogin, '/reset/', '/logout/')


weibo=Blueprint("weibo",__name__)
api=Api(weibo)
api.add_resource(Weibos, '/weibo/','/weibo/<int:message_id>/')
api.add_resource(Comments, '/weibo/<int:message_id>/comment/','/weibo/<int:message_id>/comment/<int:comment_id>/')
api.add_resource(Top10,'/weibo/top10')