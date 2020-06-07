from flask import  request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class Lecturer(Resource):
    def get(self, lec_id):
        try:
            conn = DBConn.conn().connect()
            sql_request = "select * from public.lecturer where id = {} ".format(lec_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            result = dict(zip(tuple (query.keys()) ,query.fetchone()))
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500
    def put(self, lec_id):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            sql_request = ''
            for x in json.keys():
                sql_request = ", " + str(x) + " = '" + str(json[x]) + "'" + sql_request
            sql_request = sql_request + " where id = {};".format(lec_id)
            sql_request = 'update public.lecturer set ' + sql_request[2:]
            conn = DBConn.conn().connect()
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500