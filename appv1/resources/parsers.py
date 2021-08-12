from flask_restful import reqparse

parse=reqparse.RequestParser()

parse.add_argument('username',type=str,location='json',help='错误信息如下：{error_msg}')
parse.add_argument('email',type=str,location='json',help='错误信息如下：{error_msg}')
parse.add_argument('pwd',type=str,location='json')
parse.add_argument("fields", type=str, location='args')
parse.add_argument("fields-exclude", type=str, location='args')
parse.add_argument("embed",type=str,location='args')