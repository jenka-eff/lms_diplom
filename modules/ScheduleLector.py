from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class ScheduleLector(Resource):
    def get(self, lec_id):
        try:
            conn = DBConn.conn().connect() # connect to database
            sql_request = """select schedule_id, c."name", s.lec_id, s.course_id, day_cd, "time", place, islecture, isseminar from public.schedule0 s 
            join public.course c 
            on c.id = s.course_id
                where s.lec_id = {} and is_app;""".format(lec_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request) # This line performs query and returns json result
            result = {'schedule': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500