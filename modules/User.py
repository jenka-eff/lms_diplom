from flask import request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class User(Resource):
    def get(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect() # connect to database
            sql_request = """select id from public.users where login = '{}' and "password" = '{}' and "role" = '{}';""".format(str(json['login']),str(json['password']),str(json['role']))
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            result = dict(zip(tuple (query.keys()) ,query.fetchone()))
            print('Result: ' + jsonify(result))
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            s=''
            if(str(json['role']) == 'lecturer'):
                s = """insert into public.lecturer(id) select id from public.users where login = '{}' and "password" = '{}' and "role" = '{}';""".format(str(json['login']),str(json['password']),str(json['role']))
            else:
                if(str(json['role']) == 'student'):
                    s = """insert into public.student(id) select id from public.users where login = '{}' and "password" = '{}' and "role" = '{}';""".format(str(json['login']),str(json['password']),str(json['role']))
                else:
                    if(str(json['role']) == 'admin'):
                        s = ''
                    else:
                        raise ValueError("Roles: student, lecturer, admin")
            sql_request = """insert into public.users(login, "password", "role") values('{}', '{}', '{}');""".format(str(json['login']),str(json['password']),str(json['role']))
            sql_request += s
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            response = jsonify({"result": "OK"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500