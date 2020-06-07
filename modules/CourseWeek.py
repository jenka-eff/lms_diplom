from flask import  request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class CourseWeek(Resource):
    def get(self, course_id):
        try:
            conn = DBConn.conn().connect()
            sql_request = "select * from public.course_week where course_id = {} order by week_num; ".format(course_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request) # This line performs query and returns json result
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500
    def put(self, course_id):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            sql_request = ''
            if (json['week_num'] > 15):
                raise ValueError("there are only 15 weeks in course")
            for x in json.keys():
                if (x == "week_num"):
                    sql_request = sql_request + " where week_num = " + str(json[x])
                else:
                    if(x == "is_hw"):
                        sql_request = ", " + str(x) + " = " + str(json[x]) + "" + sql_request
                    else:
                        sql_request = ", " + str(x) + " = '" + str(json[x]) + "'" + sql_request
                #sql_request = ", " + str(x) + " = '" + str(json[x]) + "'" + sql_request
            sql_request = sql_request + " and course_id = {};".format(course_id)
            sql_request = 'update public.course_week set ' + sql_request[2:]
            conn = DBConn.conn().connect()
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500