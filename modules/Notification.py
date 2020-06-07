from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from modules import DBConn


class Notification(Resource):
    def get(self, user_id):
        try:
            conn = DBConn.conn().connect()  # connect to database
            sql_request = """select id, case when from_role = 'admin' then 'администратор' when from_role = 'student' then 'студент' when from_role = 'lecturer' then 'преподаватель' when from_role = 'course' then 'курс' end as from_role, coalesce(from_name, '')as from_name, notification, ts, is_read from 
public.notification s
where to_id = {}
order by ts desc;
""".format(user_id, user_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)  # This line performs query and returns json result
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return jsonify(result)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500