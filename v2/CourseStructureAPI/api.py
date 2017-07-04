from django.http import HttpResponse
import pymongo
from course_dashboard_api.v2.dbv import *


mongo_db = MONGO_DB

""" Description: Function to get course structure of a course
    Input Parameters:
            course_name: name of the course for which course structure is required (ex. CT101.1x)
            course_run: run of the course for which course structure is required (ex. 2016-17)
            course_organization: organization of the course for which course structure is required (ex. IITBombayX)
    Output Type: JSON Dictionary of course structure, containing sections, subsections and units
    Author: Jay Goswami
    Date of Creation: 21 June 2017
"""


def get_course_structure(course_name, course_run, course_organization):
    try:
        client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected

    db_mongo = client[mongo_db]

    mongo_cursor = db_mongo.modulestore.active_versions.find({"course": course_name, "run": course_run,
                                                              "org": course_organization})

    structure = {}
    course_id = course_organization + "+" + course_name + "+" + course_run
    structure["course_id"] = str(course_id)

    try:

        course_version = mongo_cursor[0]

        published_version = course_version['versions']['published-branch']

        mongo_cursor = db_mongo.modulestore.structures.find({'_id':published_version})

        course_structures = mongo_cursor[0]['blocks']

        chapters = []

        sequentials = []

        verticals = []

        for block in course_structures:
            if block['block_type'] == 'chapter':
                chapters.append(block)
            elif block['block_type'] == 'sequential':
                sequentials.append(block)
            elif block['block_type'] == 'vertical':
                verticals.append(block)

        section = []

        for chapter in chapters:
            currentSection = {}
            currentSection["name"] = chapter["fields"]["display_name"]
            subsection = []

            for sequential in chapter["fields"]["children"]:
                currentSubsection = {}
                for currentSubSection in sequentials:
                    if currentSubSection['block_id']==sequential[1]:
                        break
                currentSubsection["name"] = currentSubSection["fields"]["display_name"]
                unit = []

                for vertical in currentSubSection["fields"]["children"]:
                    currentUnit = {}
                    for currentUNit in verticals:
                        if currentUNit["block_id"] == vertical[1]:
                            break
                    currentUnit["name"] = currentUNit["fields"]["display_name"]
                    unit.append(currentUnit)
                currentSubsection["unit"] = unit
                subsection.append(currentSubsection)

            currentSection["subsection"] = subsection
            section.append(currentSection)

        structure["section"] = section

    except:
        client.close()
        return None

        client.close()

    return structure


""" Description: Function to get course of all courses
    Input Parameters:
            None
    Output Type: List of JSON Dictionary of course structure, with each JSON containing sections, subsections and units
    Author: Jay Goswami
    Date of Creation: 21 June 2017
"""


def get_all_courses_structure():
    try:
        client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected

    db_mongo = client[mongo_db]

    mongo_cursor = db_mongo.modulestore.active_versions.find()

    courses_structure_list = []

    for course in mongo_cursor:
        course_name = course['course']
        course_run = course['run']
        course_organization = course['org']
        dict = get_course_structure(course_name, course_run, course_organization)
        courses_structure_list.append(dict)

    client.close()
    return courses_structure_list