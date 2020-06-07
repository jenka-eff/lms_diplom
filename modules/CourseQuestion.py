from flask import request
from flask_restful import Resource
import logging
from modules import DBConn


class CourseQuestion(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            user_name = ''
            sql_request = """insert into public.message(from_id, from_role, from_name, to_id, message, chain_num)
select s.id as from_id, 'student' as from_role, concat(coalesce(lastname, ''), ' ', coalesce(firstname , ''), ' ', coalesce(midname , '') ) as from_name, 
c.lec_id as to_id, '{}' as message, m.chain_num + 1
from public.student s
join public.course c 
on 1 = 1 and s.id = {} and c.id = {}
join (select coalesce(max(chain_num), 0) as chain_num from public.message) m on 1=1;
""".format(json['message'],json['student_id'], json['course_id'])
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500
