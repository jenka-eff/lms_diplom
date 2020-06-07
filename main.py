from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS, cross_origin
import logging
from collections import defaultdict
from statistics import mean
import modules._

db_connect = create_engine('postgresql://postgres:postgres@db-1.csjtwc9fnrfy.us-east-2.rds.amazonaws.com:5432/postgres')

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
logging.basicConfig(filename="sample.log", level=logging.INFO)


api.add_resource(modules.Lecturer, '/lecturer/<lec_id>')
api.add_resource(modules.LecturerCourses, '/lecturer/course/<lec_id>')
api.add_resource(modules.Lecturers, '/lecturer')
api.add_resource(modules.Student, '/student/<student_id>') # Route_1
api.add_resource(modules.Students, '/student')
api.add_resource(modules.Course, '/course')
api.add_resource(modules.CourseUpd, '/course/<course_id>')
api.add_resource(modules.CourseWeek, '/course/week/<course_id>')
api.add_resource(modules.CourseNotification, '/course/notification/<course_id>')

api.add_resource(modules.StudentNotification, '/student/notification/<student_id>')
api.add_resource(modules.CourseNotificationCreate, '/course/notification')
api.add_resource(modules.User, '/user')
api.add_resource(modules.UserAuth, '/user/auth')
api.add_resource(modules.UserUnauth, '/user/unauth/<user_id>')
api.add_resource(modules.CourseStudent, '/course/student')
api.add_resource(modules.CourseStudentName, '/course/student/<student_id>')
api.add_resource(modules.StudentCourseName, '/student/course/<course_id>')
api.add_resource(modules.CourseStudentHomework, '/course/hw')
api.add_resource(modules.CourseStudentHomeworkGet, '/course/hw/<course_id>')
api.add_resource(modules.CourseStudentHomeworkOne, '/student/course/hw')
api.add_resource(modules.CourseStudentComment, '/course/hw/comm')
api.add_resource(modules.Schedule, '/schedule')
api.add_resource(modules.ScheduleApprove, '/schedule/app/<lec_id>')
api.add_resource(modules.ScheduleUnapprove, '/schedule/unapp/<lec_id>')

api.add_resource(modules.ScheduleStudent, '/schedule/student/<student_id>')
api.add_resource(modules.ScheduleLector, '/schedule/lecturer/<lec_id>')
api.add_resource(modules.ScheduleLectorNotApp, '/schedule/lecturer/unapp/<lec_id>')


api.add_resource(modules.Notification, '/notification/<user_id>')
api.add_resource(modules.NotificationNumber, '/notification/number/<user_id>')
api.add_resource(modules.Message, '/message/<user_id>')
api.add_resource(modules.MessageNumber, '/message/number/<user_id>')
api.add_resource(modules.MessageAnswer, '/message')
api.add_resource(modules.CourseQuestion, '/course/question')

api.add_resource(modules.MessageRead, '/message/read/<mes_id>')
api.add_resource(modules.NotificationRead, '/notification/read/<mes_id>')




if __name__ == '__main__':
    app.run(host= '0.0.0.0',port='5002')