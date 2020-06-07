from flask_restful import Resource
import logging
from modules import DBConn


class ScheduleApprove(Resource):
    def post(self, lec_id):
        try:
            conn = DBConn.conn().connect()
            sql_request = """delete from public.schedule0
	where lec_id = {} and is_app = true;
	update public.schedule0
	set is_app = true 
	where lec_id = {};
    insert into public.notification( from_role, to_id, notification)
select 'admin' as from_role,  {} as to_id, 'Ваше расписание одобрено администрацией' as notification;""".format(lec_id, lec_id, lec_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500