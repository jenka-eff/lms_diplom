
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from collections import defaultdict
from modules import DBConn


class CourseStudentHomeworkGet(Resource):
    def get(self, course_id):
        try:
            conn = DBConn.conn().connect() # connect to database
            sql_request = """select student_id, week_num, mark, hw_url, "comment", lastname, midname, firstname, s."group" from public.homeworks h 
            join public.student s on h.student_id = s.id
                where course_id = {};""".format(course_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request) # This line performs query and returns json result
            result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
            grouped = defaultdict(list)
            for item in result:
                grouped[item['student_id'], item['lastname'], item['midname'], item['firstname'], item['group']].append(item)
            res = []
            for student,hw in grouped.items():
                res0 = {'student_id':student[0],'lastname':student[1],'midname':student[2],'firstname':student[3],'group':student[4]}
                for k in hw:
                    k.pop('student_id')
                    k.pop('lastname')
                    k.pop('midname')
                    k.pop('firstname')
                    k.pop('group')
                res0.update({'hw': hw})
                res.append(res0)
            return jsonify(res)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500