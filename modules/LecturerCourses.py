from flask_restful import Resource
from flask_jsonpify import jsonify
import logging
from collections import defaultdict
from modules import DBConn


class LecturerCourses(Resource):
    def get(self, lec_id):
        try:
            conn = DBConn.conn().connect() # connect to database
            sql_request = """select c.id, "name", imgurl, info, c.lec_id,
s.islecture, s.isseminar, s.day_cd, s."time" , s.place, 
concat(coalesce(lastname, ''), ' ', coalesce(firstname , ''), ' ', coalesce(midname , '') ) as teacher  from public.course c
left join schedule0 s on c.id = s.course_id and s.is_app
left join lecturer l on l.id  = c.lec_id 
where c.lec_id = {}; """.format(lec_id)
            logging.info('Request to DB: {}'.format(sql_request))
            query = conn.execute(sql_request) # This line performs query and returns json result
            result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
            grouped = defaultdict(list)
            for item in result:
                grouped[item['id'], item['name'], item['imgurl'], item['info'], item['lec_id'], item['teacher']].append(item)
            res = []
            #print(grouped.items())
            for course,sched in grouped.items():
                #print(course)
                res0 = {'id':course[0],'name':course[1],'imgurl':course[2],'info':course[3],'lec_id':course[4],'teacher':course[5]}
                for k in sched:
                    k.pop('id')
                    k.pop('name')
                    k.pop('imgurl')
                    k.pop('info')
                    k.pop('lec_id')
                    k.pop('teacher')
                res0.update({'schedule': sched})
                res.append(res0)
            res = {'data': res}
            return jsonify(res)
        except Exception as e:
            logging.info('Exception: {}'.format(e))
            return 'Exception: {}'.format(e), 500