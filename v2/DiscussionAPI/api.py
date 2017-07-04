from django.http import HttpResponse
import pymongo
from course_dashboard_api.v2.dbv import *

mongo_discussion_db = MONGO_DISCUSSION_DB

""" Description: Function to get discussion forum activity for a student - i.e. count of posts/questions
    Input Parameters:
            user: id of the student whose activity needs to be found
    Output Type: JSON Dictionary with count of posts and questions for the student
    Author: Jay Goswami
    Date of Creation: 19 June 2017
"""


def get_count_student(user):
    try:
        client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected

    db_mongo = client[mongo_discussion_db]

    pipeline = [{"$match": {"author_id": user}}, {"$group": {"_id": "$thread_type", "count": {"$sum": 1}}}]
    result =  db_mongo.contents.aggregate(pipeline)
    dict = {"user_id": user}
    list = {}
    for c in result['result']:
        list[c['_id']] = c['count']
    if list == {}:
        return None
    dict['count'] = list
    client.close()
    return dict


""" Description: Function to get discussion forum activity for all student - i.e. count of posts/questions
    Input Parameters:
            None
    Output Type: List of JSON Dictionary with count of posts and questions for all students
    Author: Jay Goswami
    Date of Creation: 19 June 2017
"""


def get_all_students_count():
    try:
        client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected

    db_mongo = client[mongo_discussion_db]

    mongo_cursor = db_mongo.contents.distinct('author_id')

    list = []

    for user in mongo_cursor:
        list.append(get_count_student(user))

    client.close()
    return list

""" Description: Function to get discussion forum activity for a student - i.e. count of posts/questions
    Input Parameters:
            user: id of the student whose activity needs to be found
    Output Type: JSON Dictionary with count of posts and questions for the student
    Author: Jay Goswami
    Date of Creation: 19 June 2017
"""


def get_count_course(course_id):
    try:
        client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected

    db_mongo = client[mongo_discussion_db]

    pipeline = [{"$match": {"course_id": course_id}}, {"$group": {"_id": "$thread_type", "count": {"$sum": 1}}}]
    result =  db_mongo.contents.aggregate(pipeline)
    dict = {"course_id": course_id}
    list = {}
    for c in result['result']:
        list[c['_id']] = c['count']
    if list == {}:
        return None
    dict['count'] = list
    client.close()
    return dict


""" Description: Function to get discussion forum activity for all student - i.e. count of posts/questions
    Input Parameters:
            None
    Output Type: List of JSON Dictionary with count of posts and questions for all students
    Author: Jay Goswami
    Date of Creation: 19 June 2017
"""


def get_all_courses_count():
    try:
        client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected

    db_mongo = client[mongo_discussion_db]

    mongo_cursor = db_mongo.contents.distinct('course_id')

    list = []

    for course in mongo_cursor:
        list.append(get_count_course(course))

    client.close()
    return list