from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class CourseStudentName(Resource):
    def get(self, student_id):
        try:
            conn = DBConn.conn().connect() # connect to database
            query = conn.execute("""select course_name, course_id, from public.v_student_course_names
                where student_id = {};""".format(student_id) ) # This line performs query and returns json result
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500