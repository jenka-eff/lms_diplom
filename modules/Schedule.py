from flask import  request
from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from collections import defaultdict
from modules import DBConn


class Schedule(Resource):
    def post(self):
        try:
            json = request.get_json()
            logging.info('Request: {}'.format(json))
            conn = DBConn.conn().connect()
            lec_id = json['lec_id']
            sql_request = """delete from public.schedule0
            where lec_id = {} and not is_app;
            insert into public.schedule0(schedule_id, lec_id, course_id, day_cd, "time", place, islecture, isseminar) select schedule_id+1, {} as lec_id, course_id, day_cd, "time", place, islecture, isseminar from (""".format(
                lec_id, lec_id)
            sql_request += " union all ".join(
                'select  {} as course_id, \'{}\' as day_cd, {} as "time", \'{}\' as place, {} as islecture, {} as isseminar'.format(
                    x['course_id'], x['day_cd'], x['time'], x['place'], x['islecture'], x['isseminar']) for x in
                json['schedule'])
            sql_request += """) a  join (select coalesce(max(schedule_id),0) as schedule_id from public.schedule0) b on 1 = 1"""
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request)
            return 'OK'
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500

    def get(self):
        try:
            sql_request = """select s.lec_id, concat(coalesce(l.lastname, ''), ' ', coalesce(l.firstname , ''), ' ', coalesce(l.midname , '') ) as "lec_name",  c."name" as "name",
s.course_id, s.day_cd, s."time", s.place, s.islecture, s.isseminar
from public.schedule0 s join lecturer l on s.lec_id = l.id 
join public.course c on s.course_id = c.id
where not is_app and s."comment" is null;"""

            logging.info('Request to DB: {}'.format(sql_request))
            conn = DBConn.conn().connect()
            query = conn.execute(sql_request)
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            grouped = defaultdict(list)
            for item in result:
                grouped[item['lec_id'], item['lec_name']].append(item)
            res = []
            for lec, sched in grouped.items():
                res0 = {'lec_id': lec[0], 'name': lec[1]}
                for k in sched:
                    k.pop('lec_name')
                res0.update({'schedule': sched})
                res.append(res0)
            return jsonify(res)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500