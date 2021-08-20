import re

from flask import url_for, flash, make_response
from flask_compress import Compress
from flask_login import login_required, current_user
from flask_restful import Resource, fields, marshal
from sqlalchemy import func, or_, text, desc
from flask_cors import cross_origin

from .login_views import user_field
from .parsers import parse
from ..database.models import Message, db, Relation, Comm

compress = Compress()


class date(fields.Raw):
    def format(self, value):
        matchobj = re.match(
            r'(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2}).*',
            str(value), re.M | re.I)
        tup = matchobj.groups()
        lis = [list(map(lambda x: int(x), tup[0:3])), list(map(lambda x: int(x), tup[3:6]))]
        return lis


comment_fields = {"id": fields.Integer, "comment_info": fields.String, "comment_date": date,
                  "user": fields.Nested(user_field)}


def order(odermethod):
    if odermethod == "comment-count,-message-date":
        return (Message.comment_count, Message.message_date.desc())
    elif odermethod == "-message-date,comment-count":
        return (Message.message_date.desc(), Message.comment_count)
    elif odermethod == "-message-date":
        return (Message.message_date.desc(),)
    else:
        return (Message.comment_count,)


def field(args):
    message_fields = {}
    message_transpond_fields = {"reference": fields.Nested(message_fields)}
    if args["fields"] is not None:
        if re.search('id', args['fields'], re.I):
            message_fields["id"] = fields.Integer
            message_transpond_fields["id"] = fields.Integer
        if re.search('info', args['fields'], re.I):
            message_fields["info"] = fields.String
            message_transpond_fields["info"] = fields.String
        # if re.search('id',args['fields'],re.I):
        #     pass
    else:
        message_fields = {"id": fields.Integer, "info": fields.String, "message_date": date,
                          "comment_count": fields.Integer, "user_id": fields.Integer}
        message_transpond_fields = {"id": fields.Integer, "info": fields.String, "message_date": date,
                                    "comment_count": fields.Integer,
                                    "user_id": fields.Integer, "reference": fields.Nested(message_fields)}
        if args["fields-exclude"] is not None:
            if re.search('id', args["fields-exclude"], re.I):
                message_fields.pop('id')
                message_transpond_fields.pop('id')
            if re.search('info', args["fields-exclude"], re.I):
                message_fields.pop('info')
                message_transpond_fields.pop('info')
        # if re.search('id',args["fields-exclude"],re.I):
        #     pass
    if args["embed"] is not None:
        user_field = {}
        if re.search('owner.id', args["embed"], re.I):
            user_field["id"] = fields.Integer
        if re.search('owner.name', args["embed"], re.I):
            user_field["username"] = fields.String
        # if re.search('owner.id',args["embed"],re.I):
        #     pass
        message_fields.pop('user_id', None)
        message_fields["owner"] = fields.Nested(user_field)
        message_transpond_fields.pop('user_id', None)
        message_transpond_fields["owner"] = fields.Nested(user_field)

    return (message_fields, message_transpond_fields)

    # if args["fields"] =="id,info":
    #     message_fields = {"id": fields.Integer, "info": fields.String}
    #     message_transpond_fields={"id": fields.Integer, "info": fields.String,"reference":fields.Nested(message_fields)}
    #     if args["embed"]=="owner.id,owner.name":
    #         user_fields={"id":fields.Integer,"username":fields.String}
    #         message_fields["owner"]=fields.Nested(user_fields)
    #         message_transpond_fields["owner"]=fields.Nested(user_fields)
    #         message_transpond_fields["reference"]=fields.Nested(message_fields)
    #     return (message_fields,message_transpond_fields)
    # elif args["fields-exclude"]=="id,info":
    #     message_fields = { "message_date": date,"comment_count": fields.Integer, "user_id": fields.Integer}
    #     message_transpond_fields = {"message_date": date,
    #                                 "comment_count": fields.Integer,
    #                                "user_id": fields.Integer, "reference": fields.Nested(message_fields)}
    #     if args["embed"] == "owner.id,owner.name":
    #         user_fields = {"id": fields.Integer, "username": fields.String}
    #         message_fields["owner"] = fields.Nested(user_fields)
    #         message_fields.pop("user_id")
    #         message_transpond_fields["owner"] = fields.Nested(user_fields)
    #         message_transpond_fields.pop("user_id")
    #         message_transpond_fields["reference"] = fields.Nested(message_fields)
    #     return (message_fields,message_transpond_fields)
    # else:
    #     message_fields = {"id":fields.Integer,"info":fields.String,"message_date": date, "comment_count": fields.Integer, "owner": fields.Nested(user_field)}
    #     message_transpond_fields = {"id":fields.Integer,"info":fields.String,"message_date": date,
    #                                 "comment_count": fields.Integer,
    #                                 "owner": fields.Nested(user_field), "reference": fields.Nested(message_fields)}
    #     return (message_fields,message_transpond_fields)


class Top10(Resource):
    @compress.compressed()
    def get(self):
        args = parse.parse_args()
        try:
            results = Message.query.order_by(Message.comment_count.desc()).limit(10).all()
        except Exception as error:
            return {"message": str(error.args), "work": False}
        else:
            # print(len(results))
            if results is not None:
                rep = marshal(results, field(args)[0], envelope="data")
                rep["work"] = True
                return rep
            else:
                return {"message": "error occurs", "work": False}


class Weibos(Resource):
    @login_required
    @compress.compressed()
    def get(self, message_id=None):
        if message_id is not None:
            args = parse.parse_args()
            try:
                result = Message.query.filter(Message.id == int(message_id)).first()
            except Exception as error:
                return {"work": False, "message": str(error.args)}
            else:
                if result is None:
                    return {"message": "message does not exist", "work": False}
                else:
                    if result.reference_id is not None:
                        rep = marshal(result, field(args)[1], envelope="data")
                        rep["work"] = True
                        rep["ref"] = True
                        return rep
                    else:
                        rep = marshal(result, field(args)[0], envelope="data")
                        rep["work"] = True
                        rep["ref"] = False
                        return rep
        else:
            parse.add_argument("deleted", type=bool, location='args')
            parse.add_argument("sort", type=str, location='args')

            args = parse.parse_args()
            # que = Message.query.outerjoin(Relation, Relation.follower_id == Message.user_id).filter(
            #     *task_filter)
            try:
                task_filter = {or_(Relation.user_id == current_user.id, Message.user_id == current_user.id)}

                que = db.session.query(Message).outerjoin(Relation, Relation.follower_id == Message.user_id).filter(
                    *task_filter)
                if args["deleted"]:
                    que = que.filter(Message.is_delete == False)

                #     # results=Message.query.filter(Message.is_delete==True).all()
                if args["sort"] is not None:
                    que = que.order_by(*order(args["sort"]))
                results = que.all()
            except Exception as error:
                return {"message": str(error.args), "work": False}
            else:
                lis = []
                # print(len(results))
                for result in results:
                    if result.reference_id is not None:
                        rep = marshal(result, field(args)[1])
                        rep["ref"] = True
                        lis.append(rep)
                    else:
                        rep = marshal(result, field(args)[0])
                        rep["ref"] = False
                        lis.append(rep)
                return {"data": lis, "work": True}
            #             results = Message.query.outerjoin(Relation, Relation.follower_id == Message.user_id).filter(
            #         *task_filter).filter(Message.is_delete==False).order_by(text(args["sort"][0],args["sort"][1])).all()
            #         else:
            #             results = Message.query.outerjoin(Relation, Relation.follower_id == Message.user_id).filter(
            #                 *task_filter).filter(Message.is_delete==False).order_by(text(args["sort"][0])).all()
            #         return marshal(results, message_transpond_fields)
            #     else:
            #
            # else:
            #     results = Message.query.outerjoin(Relation, Relation.follower_id == Message.user_id).filter(
            #         *task_filter).all()
            #     return marshal(results, message_transpond_fields)
            # for result in results:
            #     if result.reference_id is not None:
            #         lis.append(marshal(result, message_transpond_fields))
            #     else:
            #         lis.append(marshal(result, message_fields))
            # print(len(lis))
            # print(len(results))

    @login_required
    def post(self, message_id=None):
        parse.add_argument('info', type=str, location='json')
        parse.add_argument("reference_id", type=int, location='json')
        args = parse.parse_args()
        if args["reference_id"] is None:
            try:
                new_message = Message(info=args["info"], user_id=current_user.id)
                db.session.add(new_message)
                db.session.commit()
            except Exception as error:
                return {"work": False, "message": str(error.args)}
            else:
                rep = marshal(new_message, field(args)[0], envelope="data")
                rep["work"] = True
                rep["ref"] = False
                return rep
        else:
            try:
                new_message = Message(info=args["info"], user_id=current_user.id, reference_id=args["reference_id"])
                db.session.add(new_message)
                db.session.commit()
            except Exception as error:
                return {"work": False, "message": str(error.args)}
            else:
                rep = marshal(new_message, field(args)[1], envelope="data")
                rep["work"] = True
                rep["ref"] = True
                return rep

    @login_required
    def delete(self, message_id=None):
        try:
            result = Message.query.filter(Message.id == message_id).first()
        except Exception as error:
            return {"work": False, "message": str(error.args)}
        else:
            if result is not None:
                try:
                    db.session.delete(result)
                    db.session.commit()
                except Exception as error:
                    return {"work": False, "message": str(error.args)}
                else:
                    return {"work": True}
            else:
                return {"work": False, "message": "message does not exist"}

    @login_required
    def patch(self, message_id=None):
        parse.add_argument('info', type=str, location='json')
        args = parse.parse_args()
        try:
            result = Message.query.filter(Message.id == message_id).first()
        except Exception as error:
            return {"work": False, "message": str(error.args)}
        else:
            if result is not None:
                result.info = result.info + args["info"]
                result.message_date = func.now()
                try:
                    db.session.commit()
                except Exception as error:
                    return {"work": False, "message": str(error.args)}
                else:
                    if result.reference_id is not None:
                        rep = marshal(result, field(args)[1], envelope="data")
                        rep["work"] = True
                        rep["ref"] = True
                        return rep
                    else:
                        rep = marshal(result, field(args)[0], envelope="data")
                        rep["work"] = True
                        rep["ref"] = False
                        return rep
            else:
                return {"work": False, "message": "message does not exist"}

    @login_required
    def put(self, message_id=None):
        parse.add_argument('info', type=str, location='json')
        args = parse.parse_args()
        try:
            result = Message.query.filter(Message.id == message_id).first()
        except Exception as error:
            return {"work": False, "message": str(error.args)}
        else:
            if result is not None:
                result.info = args["info"]
                result.message_date = func.now()
                try:
                    db.session.commit()
                except Exception as error:
                    return {"work": False, "message": str(error.args)}
                else:
                    if result.reference_id is not None:
                        rep = marshal(result, field(args)[1], envelope="data")
                        rep["work"] = True
                        rep["ref"] = True
                        return rep
                    else:
                        rep = marshal(result, field(args)[0], envelope="data")
                        rep["work"] = True
                        rep["ref"] = False
                        return rep
            else:
                return {"work": False, "message": "message does not exist"}


class Comments(Resource):
    @login_required
    @compress.compressed()
    def get(self, message_id, comment_id=None):
        if comment_id is None:
            try:
                results = Comm.query.filter(Comm.message_id == message_id).order_by(Comm.comment_date.desc()).all()
            except Exception as error:
                return {"work": False, "message": str(error.args)}
            else:
                # print(results)
                if results is not None:
                    rep = marshal(results, comment_fields, envelope="data")
                    rep["work"] = True
                    return rep
                else:
                    return {"work": False, "message": "comment does not exist"}
        else:
            try:
                result = Comm.query.filter(Comm.id == comment_id).first()
            except Exception as error:
                return {"work": False, "message": str(error.args)}
            else:
                if result is not None:
                    rep = marshal(result, comment_fields, envelope="data")
                    rep["work"] = True
                    return rep
                else:
                    return {"work": False, "message": "comment does not exist"}

    @login_required
    def post(self, message_id, comment_id=None):
        parse.add_argument("comment_info", type=str, location='json', required=True)
        args = parse.parse_args()
        try:
            new_comment = Comm(comment_info=args["comment_info"], user_id=current_user.id, message_id=message_id)
            db.session.add(new_comment)
            db.session.commit()
        except Exception as error:
            return {"work": False, "message": str(error.args)}
        else:
            rep = marshal(new_comment, comment_fields, envelope="data")
            rep["work"] = True
            return rep

    @login_required
    def put(self, message_id, comment_id=None):
        if comment_id is not None:
            parse.add_argument("comment_info", type=str, location='json', required=True)
            args = parse.parse_args()
            try:
                result = Comm.query.filter(Comm.id == comment_id).first()
            except Exception as error:
                return {"work": False, "message": str(error.args)}
            else:
                # print(result)
                if result is not None:
                    try:
                        result.comment_info = args["comment_info"]
                        result.comment_date = func.now()
                        # result.message_id = message_id
                        db.session.commit()
                    except Exception as error:
                        return {"work": False, "message": str(error.args)}
                    else:
                        rep = marshal(result, comment_fields, envelope="data")
                        rep["work"] = True
                        return rep
                else:
                    return {"work": False, "message": "comment does not exist"}

    @login_required
    def patch(self, message_id, comment_id=None):
        parse.add_argument("comment_info", type=str, location='json', required=True)
        args = parse.parse_args()
        try:
            result = Comm.query.filter(Comm.id == comment_id).first()
        except Exception as error:
            return {"work": False, "message": str(error.args)}
        else:
            # print(result)
            if result is not None:
                try:
                    result.comment_info = result.comment_info + args["comment_info"]
                    result.comment_date = func.now()
                    # result.message_id = message_id
                    db.session.commit()
                except Exception as error:
                    return {"work": False, "message": str(error.args)}
                else:
                    rep = marshal(result, comment_fields, envelope="data")
                    rep["work"] = True
                    return rep
            else:
                return {"work": False, "message": "comment does not exist"}

    @login_required
    def delete(self, message_id, comment_id=None):
        try:
            result = Comm.query.filter(Comm.id == comment_id).first()
        except Exception as error:
            return {"work": False, "message": str(error.args)}
        else:
            if result is not None:
                try:
                    db.session.delete(result)
                    db.session.commit()
                except Exception as error:
                    return {"work": False, "message": str(error.args)}
                else:
                    return {"work": True}
            else:
                return {"work": False, "message": "comment does not exist"}
