from flask import  request
from flask_restful import Resource
import logging
from modules import DBConn


class ScheduleUnapprove(Resource):
    def post(self, lec_id):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            sql_request = """delete from public.schedule0
            where lec_id = {} and is_app = false;
            update public.schedule0
            set "comment" = '{}'
            where lec_id = {};
            insert into public.notification( from_role, to_id, notification)
select 'admin' as from_role,  {} as to_id, 'Ваше расписание не одобрено администрацией по причине: {}' as notification;""".format(lec_id,json['comment'],lec_id, lec_id,json['comment'])
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500