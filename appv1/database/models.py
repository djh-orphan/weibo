# coding: utf-8
#flask-sqlacodegen "postgresql://duan:djh660993@localhost:5432/weibo_fix"
# --outfile "D:\pycharmproject\weibo\appv1\database\models.py" --flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Comm(db.Model):
    __tablename__ = 'comm'

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    comment_info = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime(True), nullable=False,server_default=db.FetchedValue())
    message_id = db.Column(db.ForeignKey('message.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.ForeignKey('userpeople.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    message = db.relationship('Message', primaryjoin='Comm.message_id == Message.id', backref='comms')
    user = db.relationship('Userperson', primaryjoin='Comm.user_id == Userperson.id', backref='comms')



class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    info = db.Column(db.Text, nullable=False)
    message_date = db.Column(db.DateTime(True), nullable=False,server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('userpeople.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    comment_count = db.Column(db.Integer, server_default=db.FetchedValue())
    reference_id = db.Column(db.ForeignKey('message.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    is_delete = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    reference = db.relationship('Message', remote_side=[id], primaryjoin='Message.reference_id == Message.id', backref='messages')
    owner = db.relationship('Userperson', primaryjoin='Message.user_id == Userperson.id', backref='messages')


class Picture(db.Model):
    __tablename__ = 'picture'

    picturl_url = db.Column(db.Text, primary_key=True, nullable=False)
    picture_date = db.Column(db.DateTime(True))
    message_id = db.Column(db.ForeignKey('message.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)

    message = db.relationship('Message', primaryjoin='Picture.message_id == Message.id', backref='pictures')



class Relation(db.Model):
    __tablename__ = 'relation'

    relation_date = db.Column(db.DateTime(True))
    user_id = db.Column(db.ForeignKey('userpeople.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    follower_id = db.Column(db.ForeignKey('userpeople.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)

    follower = db.relationship('Userperson', primaryjoin='Relation.follower_id == Userperson.id', backref='follow_relations')
    user = db.relationship('Userperson', primaryjoin='Relation.user_id == Userperson.id', backref='userperson_relations_0')



class Userperson(db.Model):
    __tablename__ = 'userpeople'

    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    signup_date = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())
    reset_date = db.Column(db.DateTime(True))
    oldpassword = db.Column(db.String(255))
    is_activated = db.Column(db.Boolean)
    activated_link = db.Column(db.Text)
    is_reset = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    is_delete = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())


class Userinfo(Userperson):
    __tablename__ = 'userinfo'

    info = db.Column(db.Text)
    picture_url = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey('userpeople.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, index=True, server_default=db.FetchedValue())
