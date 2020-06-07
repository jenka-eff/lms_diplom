from flask import  request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class Student(Resource):
    def get(self, student_id):
        try:
            conn = DBConn.conn().connect() # connect to database
            sql_request = "select * from public.student where id = {};".format(student_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request) # This line performs query and returns json result
            result = dict(zip(tuple (query.keys()) ,query.fetchone()))
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500
    def put(self, student_id):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            #sql_request = 'update public.student(' + ', '.join((str(x) for x in json.keys())) + ') values(\'' + '\', \''.join((str(x) for x in json.values())) + '\')'
            sql_request = ''
            for x in json.keys():
                sql_request = ", " + str(x) + " = '" + str(json[x]) + "'" + sql_request
                #if (x == "id"):
                #    sql_request = sql_request + " where id = " + str(json[x]) + ";"
                #else:
                #    sql_request = ", " + str(x) + " = '" + str(json[x]) + "'" + sql_request
            sql_request = sql_request + " where id = {};".format(student_id)
            sql_request = 'update public.student set ' + sql_request[2:]
            conn = DBConn.conn().connect()
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500