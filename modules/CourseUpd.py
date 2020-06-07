from flask import  request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class CourseUpd(Resource):
    def put(self, course_id):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            sql_request = ''
            for x in json.keys():
                sql_request = ", " + str(x) + " = '" + str(json[x]) + "'" + sql_request
            sql_request = sql_request + " where id = {};".format(course_id)
            sql_request = 'update public.course set ' + sql_request[2:]
            conn = DBConn.conn().connect()
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500

    def get(self, course_id):
        try:

            conn = DBConn.conn().connect()
            sql_request1 = """select c.id, "name", imgurl, info, c.lec_id, c.ts,  coalesce(l.lastname, '') as lastname,  coalesce(l.firstname , '') as firstname,  coalesce(l.midname , '') as midname from public.course c 
            left join lecturer l on l.id  = c.lec_id 
            where c.id = {}""".format(course_id)
            logging.info('Request to DB: {}'.format(sql_request1))
            query1 = conn.execute(sql_request1)  # This line performs query and returns json result
            result = dict(zip(tuple(query1.keys()), query1.fetchone()))
            sql_request2 = """select s.islecture, s.isseminar, s.day_cd, s."time" , s.place from public.course c 
            join schedule0 s on c.id = s.course_id and s.is_app
            where c.id = {}""".format(course_id)
            logging.info('Request to DB: {}'.format(sql_request2))
            query2 = conn.execute(sql_request2)  # This line performs query and returns json result
            result0 = {'schedule': [dict(zip(tuple(query2.keys()), i)) for i in query2.cursor]}
            result.update(result0)
            return jsonify(result)



        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 50