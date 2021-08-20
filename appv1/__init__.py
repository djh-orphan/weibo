from flask import Flask
from .config import Config
from .database.models import db
from .resources.login_views import login_manager
from .resources.weibo_views import compress
from .resources import user,weibo
from flask_cors import CORS

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)
    # app.after_request(after_request)
    compress.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(user, prefix='/')
    app.register_blueprint(weibo, prefix='/')
    return app

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp