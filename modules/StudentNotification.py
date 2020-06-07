from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class StudentNotification(Resource):
    def get(self, student_id):
        try:
            conn = DBConn.conn().connect()
            query1 ="select * from public.student_notifications  where student_id = {}; ".format(student_id)
            query2 ="update public.student_notifications set is_read = true where student_id = {}; ".format(student_id)
            logging.info('Request to DB: {}'.format(query1))
            query = conn.execute(query1) # This line performs query and returns json result
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            logging.info('Request to DB: {}'.format(query2))
            query = conn.execute(query2)
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500