from flask import  request
from flask_restful import Resource
import logging
from modules import DBConn


class CourseStudent(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            query = conn.execute("""insert into public.course_students(course_id, student_id)
                values({}, {});""".format(json['course_id'], json['student_id']))
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500