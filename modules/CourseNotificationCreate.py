from flask import  request
from flask_restful import Resource
import logging
from modules import DBConn


class CourseNotificationCreate(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            sql_request = """insert into public.course_notification(course_id, notification) values({},'{}');
            insert into public.student_notifications(student_id, from_who, from_id, notification)
            select student_id, 'course', {}, '{}' from public.course_students where course_id = {};""".format(json['course_id'], json['notification'], json['course_id'], json['notification'], json['course_id'])
            conn = DBConn.conn().connect()
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500