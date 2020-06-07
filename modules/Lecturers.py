from flask import request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class Lecturers(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            sql_request = 'insert into public.lecturer(' + ', '.join(
                (str(x) for x in json.keys())) + ') values(\'' + '\', \''.join((str(x) for x in json.values())) + '\')'
            conn = DBConn.conn().connect()
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500

    def get(self):
        try:
            conn = DBConn.conn().connect()  # connect to database
            sql_request = "select * from public.lecturer;"
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)  # This line performs query and returns json result
            result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500