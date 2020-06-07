from flask import  request
from flask_restful import Resource
import logging
from modules import DBConn


class CourseStudentHomework(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            sql_request = """insert into public.homeworks(course_id, student_id, week_num, hw_url)
            values({}, {}, {}, '{}');""".format( json['course_id'], json['student_id'], json['week_num'], json['hw_url'])
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500
    def put(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            sql_request = """update public.homeworks set mark = {}
            where course_id = {} and student_id = {} and week_num = {};""".format(json['mark'], json['course_id'], json['student_id'], json['week_num'])
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500