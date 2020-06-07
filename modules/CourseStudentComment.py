from flask import request
from flask_restful import Resource
import logging
from modules import DBConn


class CourseStudentComment(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            sql_request = """update public.homeworks
            set comment = '{}'
            where course_id = {}
            and student_id = {}
            and week_num = {};""".format( json['comment'], json['course_id'], json['student_id'], json['week_num'])
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500