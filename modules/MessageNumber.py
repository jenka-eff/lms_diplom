
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class MessageNumber(Resource):
    def get(self, user_id):
        try:
            conn = DBConn.conn().connect()  # connect to database
            sql_request = """select count(*) as mes_num from 
public.message s
where to_id = {} and not is_read;""".format(user_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)  # This line performs query and returns json result
            result = dict(zip(tuple(query.keys()), query.fetchone()))
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500