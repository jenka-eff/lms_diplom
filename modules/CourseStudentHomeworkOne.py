from flask import request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from statistics import mean
from modules import DBConn


class CourseStudentHomeworkOne(Resource):
    def get(self):
        try:
            args = request.args
            conn = DBConn.conn().connect()  # connect to database
            sql_request = """select week_num, hw_url, mark, "comment" from public.homeworks h 
where course_id = {} and student_id = {};""".format(args['course_id'], args['student_id'])
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)  # This line performs query and returns json result
            result = {'hw': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            marks = []
            for a in result['hw']:
                if (type(a['mark']) == int):
                    marks.append(a['mark'])

            avg_mark = round(mean(marks), 2)
            result.update({'avg_mark': avg_mark})
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500