from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class ScheduleStudent(Resource):
    def get(self, student_id):
        try:
            conn = DBConn.conn().connect() # connect to database
            sql_request = """select lec_id, cs.course_id, day_cd, "time", place, iislecture, isseminar from 
public.schedule0 s
join public.course_students cs 
on s.course_id = cs.course_id and cs.is_app and cs.student_id = {};""".format(student_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request) # This line performs query and returns json result
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500