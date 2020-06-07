from flask import request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class UserAuth(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect() # connect to database
            sql_request1 = """select * from public.users where login = '{}' and "password" = '{}';""".format(str(json['login']),str(json['password']))
            logging.info('Request to DB: {}'.format(sql_request1))
            query = conn.execute(sql_request1)
            if ([dict(zip(tuple (query.keys()) ,i)) for i in query.cursor] == []):
                raise ValueError("invalid login or password")
            sql_request2 = """update public.users set is_auth = true where login = '{}' and "password" = '{}';""".format(str(json['login']),str(json['password']))
            logging.info('Request to DB: {}'.format(sql_request2))
            query = conn.execute(sql_request2)
            return "OK"
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500
    def get(self):
        try:
            conn = DBConn.conn().connect() # connect to database
            query = conn.execute("""select id, role from public.users where is_auth;""")
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500