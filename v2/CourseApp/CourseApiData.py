import pymongo
from pprint import pprint
from django.http import HttpResponse
from datetime import datetime
import MySQLdb
from course_dashboard_api.v2.dbv import *
sql_user = MYSQL_USER
sql_pswd = MYSQL_PSWD
sql_db = MYSQL_DB
mongodb = MONGO_DB
mysqlFlag = False
mongoFlag = False
db_mysql = None
mongo_client = None
def connect():
    try:
        global db_mysql
        db_mysql = MySQLdb.connect(user=sql_user, passwd=sql_pswd, db=sql_db)  # Establishing MySQL connection
        global mysqlFlag
        mysqlFlag = True
    except:
        print "MySQL connection not established"
        return HttpResponse("Mysql connection not established")

    try:
        global mongo_client
        mongo_client = pymongo.MongoClient()  # Establishing MongoDB connection
        global mongoFlag
        mongoFlag = True
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected
def disconnect():

    try:
        db_mysql.close()
        mongo_client.close()
    except:
        None

""" Description: Function to Get grading policy of a Course
    Input Parameters:
            CourseDefinition  
    Output Type: JSON of Course Grading Policy
    Author: Dhruv Thakker
    Date of Creation: 21 June 2017
"""
def get_grading_policy(course_defination_id):


    connect()

    db_mongo = mongo_client[mongodb]
    mongo_cursor = db_mongo.modulestore.definitions.find({'_id': course_defination_id})
    course_definition = mongo_cursor[0]
    grading_policy = {}
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
            # print "No grade cutoffs mentioned"
    except:
        grading_policy["grade_cutoffs"] = {}
        grading_policy["grader"] = []

    disconnect()

    return grading_policy
        # print "No grading policy found"


def get_course_summary(course_name,course_run,course_org,details = False):

    connect()

    db_mongo = mongo_client[mongodb]
    mongo_cursor = db_mongo.modulestore.active_versions.find({"course": course_name, "run": course_run,
                                                              "org": course_org})
    mysql_cursor = db_mysql.cursor()
    course_team_query = "SELECT user_id,role FROM student_courseaccessrole where course_id = %s"
    course_staff_detail_query = "SELECT username,email FROM auth_user where id = %s"

    course_student_count_query = "select COUNT(user_id) from student_courseenrollment where binary course_id = %s"

    course_course = mongo_cursor[0]
    try:
        published_version = course_course['versions']['published-branch']
    except:
        return None

    mongo_cursor = db_mongo.modulestore.structures.find({'_id': published_version})

    course_structures = mongo_cursor[0]['blocks']

    for block in course_structures:
        if block['block_type'] == 'course':
            course_block = block
    try:
        course_start = course_block['fields']['start']
    except:
        course_start = None
    try:
        course_end = course_block['fields']['end']
    except:
        course_end = None

    try:
        course_registration_start = course_block['fields']['enrollment_start']
    except:
        course_registration_start = None

    try:
        course_registration_end = course_block['fields']['enrollment_end']
    except:
        course_registration_end = None

    try:
        course_organization = course_course['org']
    except:
        course_organization = None

    try:
        course_id = course_course['course']
    except:
        course_id = None

    try:
        course_run = course_course['run']
    except:
        course_run = None

    try:
        course_display_name = course_block['fields']['display_name']
    except:
        course_display_name = None
    course_id = "course-v1:" + course_organization + "+" + course_id + "+" + course_run

    try :  #<-Last Edit
        mysql_cursor.execute(course_student_count_query, (str(course_id),))
        course_student_count = mysql_cursor.fetchall()[0][0]
    except:
        course_student_count = None


    if course_start != None and course_end != None:
        if course_start > datetime.now():
            course_status = "upcoming"
        else:
            if course_end < datetime.now():
                course_status = "archived"
            else:
                course_status = "ongoing"
    else:
        course_status = "undefined"

    mysql_cursor.execute(course_team_query, (str(course_id),))
    course_team_list = mysql_cursor.fetchall()
    course_team = {}
    course_team['course_instructors'] = []
    course_staffs = []
    for item in course_team_list:
        mysql_cursor.execute(course_staff_detail_query, (item[0],))
        course_staff_detail = mysql_cursor.fetchall()[0]
        mcourse_staff_detail = {}
        mcourse_staff_detail['username'] = course_staff_detail[0]
        mcourse_staff_detail['email'] = course_staff_detail[1]
        if item[1] == 'instructor':
            course_team["course_instructors"].append(mcourse_staff_detail)
        else:
            course_staffs.append(mcourse_staff_detail)
    course_team["course_members"] = course_staffs


    course_details = {}
    course_details["course_start"] = course_start;
    course_details["course_end"] = course_end;
    course_details["course_registration_start"] = course_registration_start;
    course_details["course_registration_end"] = course_registration_end;
    course_details["course_id"] = course_id;
    course_details["course_display_name"] = course_display_name;
    course_details["course_status"] = course_status;
    course_details["course_team"] = course_team
    course_details["course_student_count"] = course_student_count #<- Last Edit

    if details :
        ## Getting Grading Policy
        definition_id = course_block['definition']
        grading_policy = get_grading_policy(definition_id)
        course_details["course_grading_policy"] = grading_policy

    disconnect()

    return course_details


def get_summary_by_faculty_name(faculty_username,details = False):

    connect()

    faculty_id_query = "SELECT id FROM auth_user where username = %s"
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(faculty_id_query, (faculty_username,))
    faculty_course_list = []
    try:
        faculty_id = mysql_cursor.fetchall()[0][0];
        faculty_course = get_summary_by_faculty_id(faculty_id , details)
        faculty_course_list.append(faculty_course)
    except:
        faculty_course_list = []

    disconnect()

    return faculty_course_list


def get_summary_by_faculty_id(faculty_id,details = False):

    connect()

    faculty_courses_query = "SELECT student_courseaccessrole.user_id, GROUP_CONCAT(student_courseaccessrole.course_id) FROM student_courseaccessrole WHERE student_courseaccessrole.role = 'instructor' and user_id = %s GROUP BY student_courseaccessrole.user_id"
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(faculty_courses_query,(faculty_id,) )
    faculty_course_list = mysql_cursor.fetchall()[0]

    faculty_course = {}
    faculty_id = faculty_course_list[0]
    course_faculty_detail_query = "SELECT username,email FROM auth_user where id = %s"
    mysql_cursor.execute(course_faculty_detail_query, (str(faculty_id),))
    faculty_detail = mysql_cursor.fetchall()[0]

    faculty_course['faculty_id'] = faculty_id;
    faculty_course['faculty_username'] = faculty_detail[0]
    faculty_course['faculty_email'] = faculty_detail[1]
    faculty_course['faculty_course_list'] = []
    course_list = faculty_course_list[1].split(',')

    for course in course_list:
        my_course = course.split(':')[1].split('+')
        try:
            course_org = my_course[0]
            course_name = my_course[1]
            course_run = my_course[2]
            faculty_course['faculty_course_list'].append(get_course_summary(course_name, course_run, course_org,details))
        except:
            continue

    disconnect()

    return faculty_course


def get_summary_facultywise(details = False):

    connect()

    facultywise_course_details =[]
    faculty_courses_query = "SELECT student_courseaccessrole.user_id FROM student_courseaccessrole WHERE student_courseaccessrole.role = 'instructor' GROUP BY student_courseaccessrole.user_id"
    mysql_cursor = db_mysql.cursor()

    mysql_cursor.execute(faculty_courses_query,)

    faculty_id_list = mysql_cursor.fetchall()

    for faculty_id in faculty_id_list:

        faculty_id =faculty_id[0]
        faculty_course = get_summary_by_faculty_id(faculty_id,details)
        facultywise_course_details.append(faculty_course)

    disconnect()

    return facultywise_course_details


def get_all_course_info(details=False):

    connect()

    course_info_list = []
    db_mongo = mongo_client[mongodb]
    mongo_cursor = db_mongo.modulestore.active_versions.find()

    for course_course in mongo_cursor:

        try:
            course_org = course_course['org']
        except:
            course_org = None

        try:
            course_name = course_course['course']
        except:
            course_name = None

        try:
            course_run = course_course['run']
        except:
            course_run = None

        course_summary = get_course_summary(course_name,course_run,course_org,details)
        if course_summary == None:
            continue
        course_info_list.append(course_summary)

    disconnect()

    return course_info_list


def get_courses_with_status(status="all",details=False):

    connect()

    course = get_all_course_info(details)

    course_required_list = []

    if status == "all":
        course_required_list = course
    else :
        for summary in course :
            try :
                if summary["course_status"] == status:
                    course_required_list.append(summary)
            except:
                continue

    disconnect()

    return course_required_list


def get_course_team(course_id):

    connect()

    instructors_query = "select user_id FROM student_courseaccessrole WHERE role = 'instructor' AND BINARY course_id = %s "
    members_query = "select user_id FROM student_courseaccessrole WHERE NOT role = 'instructor' AND BINARY course_id = %s "
    name_query = "select email from auth_user where id =%s"

    course_team = {};
    course_team['course_id'] = course_id
    course_team['course_instructors'] = []
    course_team['course_members'] = []

    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(instructors_query, (str(course_id),))
    instructors= mysql_cursor.fetchall()

    for instructor in instructors :
        mysql_cursor1 = db_mysql.cursor()
        mysql_cursor1.execute(name_query, (instructor[0],))
        instr = mysql_cursor1.fetchall()
        course_team['course_instructors'].append(instr[0][0])

    mysql_cursor.execute(members_query, (str(course_id),))
    members = mysql_cursor.fetchall()

    for member in members :
        mysql_cursor1 = db_mysql.cursor()
        mysql_cursor1.execute(name_query, (member[0],))
        mem = mysql_cursor1.fetchall()
        course_team['course_members'].append(mem[0][0])

    disconnect()

    return course_team


def get_all_course_teams(user_id):

    connect()

    courses_query    ="select distinct(course_id) from student_courseaccessrole where user_id = %s AND course_id like %s "
    cou = 'course%'
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(courses_query,(user_id,cou,))
    courses = mysql_cursor.fetchall()

    course_teams_list = []
    for course in courses:
        course_team = get_course_team(course[0])
        course_teams_list.append(course_team)

    disconnect()

    return course_teams_list


def get_course_cohort_details(course_id):

    connect ()

    cohorts_query  = "SELECT id,name FROM course_groups_courseusergroup WHERE BINARY course_id = %s "
    students_query = "SELECT user_id FROM course_groups_cohortmembership WHERE course_user_group_id = %s"
    name_query     = "SELECT username FROM auth_user WHERE id = %s "
    cohort_type_query = "SELECT assignment_type FROM course_groups_coursecohort WHERE course_user_group_id = %s"

    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(cohorts_query, (str(course_id),))
    cohorts = mysql_cursor.fetchall()
    course_cohort_list = []
    for cohort in cohorts:
        mysql_cursor1 = db_mysql.cursor()
        mcohort = {}
        mcohort['cohort_id']   =  cohort[0]
        mcohort['cohort_name'] =  cohort[1]

        mysql_cursor1.execute(cohort_type_query, (str(cohort[0]),))
        cohort_type = mysql_cursor1.fetchall()[0][0]

        mcohort['cohort_type'] = cohort_type

        mcohort['cohort_student_list'] = []

        mysql_cursor1.execute(students_query,(str(cohort[0]),) )
        cohort_students = mysql_cursor1.fetchall()
        #mcohort['cohort_student_list'] = {}
        for student in cohort_students :
            mysql_cursor2 = db_mysql.cursor()

            mstudent = {}
            mstudent['id'] = student[0]

            #id = student[0]

            mysql_cursor2.execute(name_query, (str(student[0]),))
            student_name = mysql_cursor2.fetchall()[0][0]

            mstudent['username'] = student_name
            #mcohort['cohort_student_list'][id] = student_name

            mcohort['cohort_student_list'].append(mstudent)
        course_cohort_list.append(mcohort)


    disconnect()
    return course_cohort_list


def get_all_courses_cohorts():

    connect()

    course_cohort_query = "SELECT DISTINCT( course_id ) FROM course_groups_courseusergroup"
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(course_cohort_query)
    courses = mysql_cursor.fetchall()
    courses_cohorts_list = []

    for course in courses :
        course_cohort_object = {}
        course_cohort_object['course_id'] = course[0]

        course_cohort_object['course_cohorts_list'] = get_course_cohort_details(course[0])
        courses_cohorts_list.append(course_cohort_object)

    disconnect()
    return courses_cohorts_list

#pprint (get_all_courses_cohorts())

#print MYSQL_DB
