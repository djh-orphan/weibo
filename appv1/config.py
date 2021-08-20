import os


class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "postgresql://duan:djh660993@192.144.210.195:5432/weibo_fix"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    COMPRESS_REGISTER = False
    COMPRESS_ALGORITHM = ['gzip']
    COMPRESS_LEVEL = 6
    LOIN_VIEW = "login"
    LOGIN_MESSAGE = "Unauthorized User"
    LOGIN_MESSAGE_CATEGORY = "info"
    CORS_ORIGINS = '*'
    CORS_ALLOW_HEADERS = '*'
    SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_METHODS = '*'
