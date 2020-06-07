
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class CourseNotification(Resource):
    def get(self, course_id):
        try:
            conn = DBConn.conn().connect()
            sql_request = "select course_id, notification, ts from public.course_notification  where course_id = {} ".format(course_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request) # This line performs query and returns json result
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500