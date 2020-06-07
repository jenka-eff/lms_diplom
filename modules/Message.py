from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from collections import defaultdict
from modules import DBConn


class Message(Resource):
    def get(self, user_id):
        try:
            conn = DBConn.conn().connect()  # connect to database
            sql_request1 = """select message,m.id, m.ts, is_read, chain_num 
,concat(coalesce(l.lastname, coalesce(s.lastname, '')), ' ', coalesce(l.firstname , coalesce(s.firstname , '')), ' ', coalesce(l.midname , coalesce(s.midname , '')) ) as from_name
,concat(coalesce(l2.lastname, coalesce(s2.lastname, '')), ' ', coalesce(l2.firstname , coalesce(s2.firstname , '')), ' ', coalesce(l2.midname , coalesce(s2.midname , '')) ) as to_name
from public.message m
left join public.lecturer l on m.from_id = l.id 
left join public.student s on m.from_id = s.id
left join public.lecturer l2 on m.to_id = l2.id 
left join public.student s2 on m.to_id = s2.id
where to_id = {} or from_id = {}
order by ts desc;
""".format(user_id, user_id)
            logging.info('Request to DB: {}'.format(sql_request1))
            query = conn.execute(sql_request1)
            #            sql_request2 = """
            # update public.message
            # set is_read = true
            # where to_id = {};
            # """.format( user_id)
            #            logging.info('Request to DB: {}'.format(sql_request2))
            #            query2 = conn.execute(sql_request2)
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            grouped = defaultdict(list)
            for item in result:
                grouped[item['chain_num']].append(item)
            res = {}
            for chain_num, msg in grouped.items():
                res0 = {str(chain_num): msg}
                res.update(res0)
            return jsonify(res)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500