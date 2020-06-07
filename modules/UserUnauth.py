from flask import request
from flask_restful import Resource
import logging
from modules import DBConn


class UserUnauth(Resource):
    def post(self, user_id):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()  # connect to database
            query = conn.execute("""update public.users set is_auth = false where id = '{}';""".format(user_id))
            return "OK"
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500

    def put(self):
        json = request.get_json()
        logging.info('Request: {}'.format(json))
        sql_request = "update public.users set \'' + '\', \'' .join(str(key) + '\'= \''+ str(d[key]) for key in d ) + '\' where id = %d'"
        query = conn.execute("update public.users set \'" + "\', \'".join(
            str(key) + '\'= \'' + str(d[key]) for key in d) + "\' where id = %d'" % d['id'])