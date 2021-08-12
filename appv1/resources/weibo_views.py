import re

from flask import url_for, flash, make_response
from flask_compress import Compress
from flask_login import login_required, current_user
from flask_restful import Resource, fields, marshal
from sqlalchemy import func, or_, text, desc

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
        results = Message.query.order_by(Message.comment_count.desc()).limit(10).all()
        # print(len(results))
        return marshal(results, field(args)[0])


class Weibos(Resource):
    @login_required
    @compress.compressed()
    def get(self, message_id=None):
        if message_id is not None:
            args = parse.parse_args()
            result = Message.query.filter(Message.id == int(message_id)).first()
            if result is None:
                return None
            else:
                if result.reference_id is not None:
                    return make_response(marshal(result, field(args)[1]))
                else:
                    return make_response(marshal(result, field(args)[0]))
        else:
            parse.add_argument("deleted", type=bool, location='args')
            parse.add_argument("sort", type=str, location='args')

            args = parse.parse_args()
            task_filter = {or_(Relation.user_id == current_user.id, Message.user_id == current_user.id)}
            # que = Message.query.outerjoin(Relation, Relation.follower_id == Message.user_id).filter(
            #     *task_filter)
            que = db.session.query(Message).outerjoin(Relation, Relation.follower_id == Message.user_id).filter(
                *task_filter)
            if args["deleted"]:
                que = que.filter(Message.is_delete == False)

            #     # results=Message.query.filter(Message.is_delete==True).all()
            if args["sort"] is not None:
                que = que.order_by(*order(args["sort"]))
            results = que.all()
            lis = []
            # print(len(results))
            for result in results:
                if result.reference_id is not None:
                    lis.append(marshal(result, field(args)[1]))
                else:
                    lis.append(marshal(result, field(args)[0]))
            return lis
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
            new_message = Message(info=args["info"], user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            return marshal(new_message, field(args)[0])
        else:
            new_message = Message(info=args["info"], user_id=current_user.id, reference_id=args["reference_id"])
            db.session.add(new_message)
            db.session.commit()
            return marshal(new_message, field(args)[1])

    @login_required
    def delete(self, message_id=None):
        result = Message.query.filter(Message.id == message_id).first()
        if result is not None:
            db.session.delete(result)
            db.session.commit()
            return True
        else:
            return False

    @login_required
    def patch(self, message_id=None):
        parse.add_argument('info', type=str, location='json')
        args = parse.parse_args()
        result = Message.query.filter(Message.id == message_id).first()
        if result is not None:
            result.info = result.info + args["info"]
            result.message_date = func.now()
            db.session.commit()
            if result.reference_id is not None:
                return make_response(marshal(result, field(args)[1]))
            else:
                return make_response(marshal(result, field(args)[0]))
        else:
            return False

    @login_required
    def put(self, message_id=None):
        parse.add_argument('info', type=str, location='json')
        args = parse.parse_args()
        result = Message.query.filter(Message.id == message_id).first()
        if result is not None:
            result.info = args["info"]
            result.message_date = func.now()
            db.session.commit()
            if result.reference_id is not None:
                return make_response(marshal(result, field(args)[1]))
            else:
                return make_response(marshal(result, field(args)[0]))
        else:
            return False


class Comments(Resource):
    @login_required
    @compress.compressed()
    def get(self, message_id, comment_id=None):
        if comment_id is None:
            results = Comm.query.filter(Comm.message_id == message_id).order_by(Comm.comment_date.desc()).all()
            # print(results)
            if results is not None:
                return marshal(results, comment_fields)
            else:
                return None
        else:
            result = Comm.query.filter(Comm.id == comment_id).first()
            if result is not None:
                return marshal(result, comment_fields)
            else:
                return None

    @login_required
    def post(self, message_id, comment_id=None):
        parse.add_argument("comment_info", type=str, location='json', required=True)
        args = parse.parse_args()
        new_comment = Comm(comment_info=args["comment_info"], user_id=current_user.id, message_id=message_id)
        db.session.add(new_comment)
        db.session.commit()
        return marshal(new_comment, comment_fields)

    @login_required
    def put(self, message_id, comment_id=None):
        if comment_id is not None:
            parse.add_argument("comment_info", type=str, location='json', required=True)
            args = parse.parse_args()
            result = Comm.query.filter(Comm.id == comment_id).first()
            # print(result)
            if result is not None:
                result.comment_info = args["comment_info"]
                result.comment_date = func.now()
                # result.message_id = message_id
                db.session.commit()
                return marshal(result, comment_fields)
            else:
                return False

    @login_required
    def patch(self, message_id, comment_id=None):
        parse.add_argument("comment_info", type=str, location='json', required=True)
        args = parse.parse_args()
        result = Comm.query.filter(Comm.id == comment_id).first()
        if result is not None:
            result.comment_info = result.comment_info + args["comment_info"]
            result.comment_date = func.now()
            db.session.commit()
            return marshal(result, comment_fields)
        else:
            return False

    @login_required
    def delete(self, message_id, comment_id=None):
        result = Comm.query.filter(Comm.id == comment_id).first()
        if result is not None:
            db.session.delete(result)
            db.session.commit()
            return True
        else:
            return False
