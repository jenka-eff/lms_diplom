from flask import  request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class Course(Resource):
    #####
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            sql_request = 'insert into public.course(' + ', '.join(
                (str(x) for x in json.keys())) + ') values(\'' + '\', \''.join((str(x) for x in json.values())) + '\');'
            sql_request += """insert into public.course_week(course_id, week_num)
select course_id, a from 
(select 1 as a union all 
select 2 as a union all 
select 3 as a union all 
select 4 as a union all 
select 5 as a union all 
select 6 as a union all 
select 7 as a union all 
select 8 as a union all 
select 9 as a union all 
select 10 as a union all 
select 11 as a union all 
select 12 as a union all 
select 13 as a union all 
select 14 as a union all 
select 15 as a) s join(select max(id) as course_id from public.course where "name" = '{}' and lec_id = {} ) d on 1=1;
""".format(json['name'], json['lec_id'])
            conn = DBConn.conn().connect()
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500

    def get(self):
        try:
            conn = DBConn.conn().connect()
            sql_request = """select * from public.course;"""
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)  # This line performs query and returns json result
            result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500