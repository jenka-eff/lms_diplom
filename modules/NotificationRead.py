from flask import request
from flask_restful import Resource
import logging
from modules import DBConn


class NotificationRead(Resource):
    def post(self, mes_id):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            sql_request2 = """
update public.notification
set is_read = true
where id = {};
""".format(mes_id)
            logging.info('Request to DB: {}'.format(sql_request2))
            query2 = conn.execute(sql_request2)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500
