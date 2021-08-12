from flask import Flask
from .config import Config
from .database.models import db
from .resources.login_views import login_manager
from .resources.weibo_views import compress
from .resources import user,weibo

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    compress.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(user, prefix='/')
    app.register_blueprint(weibo, prefix='/')
    return app