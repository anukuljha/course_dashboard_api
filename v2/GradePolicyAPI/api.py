from django.http import HttpResponse
import pymongo
from course_dashboard_api.v2.dbv import *

mongo_db = MONGO_DB

""" Description: Function to get grading policy of a course
    Input Parameters:
            course_name: name of the course for which grading policy is required (ex. CT101.1x)
            course_run: run of the course for which grading policy is required (ex. 2016-17)
            course_organization: organization of the course for which grading policy is required (ex. IITBombayX)
    Output Type: JSON Dictionary with course details and grading policy and cutoffs
    Author: Jay Goswami
    Date of Creation: 31 May 2017
"""


def get_grading_policy(course_name, course_run, course_organization):
    try:
        client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected

    db_mongo = client[mongo_db]

    mongo_cursor = db_mongo.modulestore.active_versions.find({"course": course_name, "run": course_run,
                                                              "org": course_organization})

    grading_policy = {}
    course_id = course_organization + "+" + course_name + "+" + course_run
    grading_policy["course_id"] = str(course_id)
    grading_policy["name"] = course_name
    grading_policy["run"] = course_run
    grading_policy["organization"] = course_organization

    try:

        course_version = mongo_cursor[0]

        try:

            published_version = course_version['versions']['published-branch']

            mongo_cursor = db_mongo.modulestore.structures.find({'_id':published_version})

            course_structures = mongo_cursor[0]['blocks']
            for block in course_structures:
                if block['block_type'] == 'course':
                    course_block = block
            try:
                course_start = course_block['fields']['start']
                grading_policy["course_start"] = str(course_start.date())
            except:
                grading_policy["course_start"] = ""
                #print "Course start date not found"
            try:
                course_end = course_block['fields']['end']
                grading_policy["course_end"] = str(course_end.date())
            except:
                grading_policy["course_end"] = ""
                #print "Course end date not found"
            try:
                course_registration_start = course_block['fields']['enrollment_start']
                grading_policy["course_registration_start"] = str(course_registration_start.date())
            except:
                grading_policy["course_registration_start"] = ""
                #print "Course registration start date not found"
            try:
                course_registration_end = course_block['fields']['enrollment_end']
                grading_policy["course_registration_end"] = str(course_registration_end.date())
            except:
                grading_policy["course_registration_end"] = ""
                #print "Course registration end date not found"

            try:
                course_display_name = course_block['fields']['display_name']
                grading_policy["course_display_name"] = str(course_display_name)
            except:
                grading_policy["course_display_name"] = ""
                #print "Course display name not found"

            definition_id = course_block['definition']
            mongo_cursor = db_mongo.modulestore.definitions.find({'_id':definition_id})
            course_definition = mongo_cursor[0]

            try:
                grade_list = course_definition['fields']['grading_policy']['GRADER']
                grader_result_list = []

                for j in range(len(grade_list)):
                    grader_result_dict = {}
                    min_count = grade_list[j]['min_count']
                    drop_count = grade_list[j]['drop_count']
                    short_label = grade_list[j]['short_label']
                    display_name = grade_list[j]['type']
                    weight = grade_list[j]['weight']
                    grader_result_dict["min_count"] = min_count
                    grader_result_dict["drop_count"] = drop_count
                    grader_result_dict["short_label"] = str(short_label)
                    grader_result_dict["type"] = str(display_name)
                    grader_result_dict["weight"] = weight
                    grader_result_list.append(grader_result_dict)
                grading_policy["grader"] = grader_result_list
                try:
                    grade_cutoffs = course_definition['fields']['grading_policy']['GRADE_CUTOFFS']
                    grading_policy["grade_cutoffs"] = grade_cutoffs
                except:
                    grading_policy["grade_cutoffs"] = {}
                    #print "No grade cutoffs mentioned"
            except:
                grading_policy["grade_cutoffs"] = {}
                grading_policy["grader"] = []
                #print "No grading policy found"
        except:
            grading_policy["course_start"] = ""
            grading_policy["course_end"] = ""
            grading_policy["course_registration_start"] = ""
            grading_policy["course_registration_end"] = ""
            grading_policy["course_display_name"] = ""
            grading_policy["grade_cutoffs"] = {}
            grading_policy["grader"] = []
            #print "Course not found"
    except:
        client.close()
        return None

    client.close()

    return grading_policy


""" Description: Function to get grading policy of all courses
    Input Parameters:
            None
    Output Type: List of JSON Dictionary with each JSON containing course details and grading policy and cutoffs
    Author: Jay Goswami
    Date of Creation: 9 June 2017
"""


def get_all_courses_grading_policy():
    try:
        client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected

    db_mongo = client[mongo_db]

    mongo_cursor = db_mongo.modulestore.active_versions.find()

    courses_grade_policy_list = []

    for course in mongo_cursor:
        course_name = course['course']
        course_run = course['run']
        course_organization = course['org']
        dict = get_grading_policy(course_name, course_run, course_organization)
        courses_grade_policy_list.append(dict)

    client.close()
    return courses_grade_policy_list