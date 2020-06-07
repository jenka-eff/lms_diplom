from flask import  request
from flask_restful import Resource
import logging
from modules import DBConn


class MessageAnswer(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            sql_request = """insert into public.message(chain_num, from_id, to_id, message)
select distinct chain_num, from_id, {} as to_id, '{}' as message from message 
where chain_num = {} and from_id <> {}
;""".format(json['user_id'],json['message'],json['chain_num'], json['user_id'])
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500