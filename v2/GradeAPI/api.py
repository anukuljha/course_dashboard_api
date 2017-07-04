from django.http import HttpResponse
import pymongo
import MySQLdb
from course_dashboard_api.v2.dbv import *

sql_user = MYSQL_USER
sql_pswd = MYSQL_PSWD
mysql_db = MYSQL_DB
mongo_db = MONGO_DB

""" Description: Function to get quiz level grades of all students in a particular course.
    Input Parameters:
            course_name: name of the course for which grades are required (ex. CT101.1x)
            course_run: run of the course for which grades are required (ex. 2016-17)
            course_organization: organization of the course for which grades are required (ex. IITBombayX)
    Output Type : List of grades of all students enrolled in the course
    Author: Jay Goswami
    Date of creation: 30 May 2017
"""


def get_all_student_grades(course_name, course_run, course_organization):
    student_count = 1
    try:
        mongo_client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established") # MongoDB could not be connected
    try:
        db_mysql = MySQLdb.connect(user=sql_user, passwd=sql_pswd, db=mysql_db) # Establishing MySQL connection
    except:
        print "MySQL connection not established"
        return HttpResponse("MySQL connection not established") # MySQL could not be connected
    full_grade_list = []
    problem_query = "Select grade,max_grade from courseware_studentmodule where max_grade is not null and grade is not null and student_id=%s and binary module_id=%s"
    users_query = "select a.id, a.username, a.email, b.course_id from auth_user as a, student_courseenrollment as b where a.id=b.user_id"
    # Query to retrieve the details of all students who have enrolled in any course

    grading_policy = get_grading_policy(course_name, course_run, course_organization)
    try:
        grading_list = grading_policy['grader']
        grade_cutoffs = grading_policy['grade_cutoffs']
    except:
        return None
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(users_query)
    student_course_list = mysql_cursor.fetchall()
    for student_course_pair in student_course_list:
        found_course_id = student_course_pair[3].split(':')
        if len(found_course_id)==1:
            continue
        course_id = course_organization + '+' + course_name + '+' + course_run
        if course_id == found_course_id[1]:  # Comparing course_id to get students enrolled in a particular course
            student_grades = get_student_course_grades(str(student_course_pair[2]), str(student_course_pair[1]),
                                                    int(student_course_pair[0]), course_name, course_run, course_organization, student_count, db_mysql,
                                                    mongo_client, problem_query, grading_list, grade_cutoffs)  # Calling function to get quiz grades of each student
            student_count += 1   # Increment the count of students
            full_grade_list.append(student_grades)  # Appending student's grade list

    mongo_client.close()  # Closing MongoDB connection
    db_mysql.close()  # Closing MySQL connection
    grade_list = {}
    grade_list['course_name'] = course_name
    grade_list['course_organization'] = course_organization
    grade_list['course_run'] = course_run
    grade_list['students'] = full_grade_list
    return grade_list


""" Description: Function to get quiz level grades of each student in a particular course.This function is called by function get_all_student_grades().
    Input Parameters:
            email: Email id of student passed to this function by get_all_student_grades()
            student_name: Username of student passed to this function by get_all_student_grades() 
            student_id: User ID of a student
            course_id: ID of course for which grades are to be calculated
            course_run: run of the course for which grades are to be calculated
            course_organization: organization of the course for which grades are to be calculated
            count: Number of students in the course including current student
            db_mysql: MySQL Database connection object
            mongo_client: MongoDB connection object
            problem_query: Query passed to this function by get_all_student_grades()
    Output Type: List
    Author: Jay Goswami
    Date of Creation: 30 May 2017
"""


def get_student_course_grades(email, student_name, student_id, course_id, course_run, course_organization, count, db_mysql, mongo_client, problem_query, grading_list, grade_cutoffs):
    highchart_list = []  # List to be returned for highcharts
    highchart_list2 = []  # List to be returned for highcharts
    highchart_list3 = {}
    highchart_list.append('total_score')
    highchart_list3['id'] = student_id
    highchart_list3['name'] = student_name
    highchart_list3['email'] = email
    db_mongo = mongo_client[mongo_db]  # Getting the object for edxapp database of MongoDB

    mongo_cur = db_mongo.modulestore.active_versions.find({"course":course_id, "run":course_run, "org":course_organization}) # Find the
    i = mongo_cur[0]
    active_version = mongo_cur[0]
    version = i["versions"]["published-branch"]

    try:
        stud_avg_tot = 0
        completed = True

        for j in range(len(grading_list)):  # iterating over the formats
            best_score_list = []  # This list will store the final scores for the particular format
            drop_count = grading_list[j]['drop_count']  # Gives number of droppable sections for that problem
            type = grading_list[j]['type']  # Gives the type of the format i.e. Quiz, Final Exam etc.
            short_label = grading_list[j]['short_label']
            weight = grading_list[j]['weight']  # Gives the weights of the formats
            min_count = grading_list[j]['min_count']  # Gives the minimum number of sections of that type present in the course
            mongo_cur2 = db_mongo.modulestore.structures.find({'_id': version})
            blocks = mongo_cur2[0]['blocks']
            mongo_cur2 = []
            for block in blocks:
                if 'format' in block['fields'] and block['fields']['format']==type and block['fields']['graded']==True:
                   mongo_cur2.append(block)
            count_doc = len(mongo_cur2)
            # Query to find the different sequentials having the format 'type'
            sequential_coun = 0  # intializing sequential count to zero
            for k in mongo_cur2:
                sequential_coun += 1
                avg_score_sequential = 0
                sum_avg_prob_score = 0
                sum_prob_score_obt = 0
                sum_tot_prob_score = 0
                coun_prob = 0  # Initializing problem count as zero
                list2 = k['fields'][
                   'children']  # Getting the children list of the sequential, this will consist of vertical ids
                for m in range(len(list2)):  # Iterating over the list of vertical ids
                    child_id = list2[m]  # Getting the vertical id
                    vertical_id = child_id[1]

                    mongo_cur3 = []
                    for block in blocks:
                        if block['block_id']==vertical_id: # query to get the vertical document with the _id.name as vertical id
                            mongo_cur3.append(block)

                    n = mongo_cur3[0]
                    list3 = n['fields']['children']  # getting the children array for this vertical, consisiting of list of component ids
                    for o in range(len(list3)):  # Iterating over the list of component ids
                        comp_id = list3[o]  # Getting the component id
                        component_id = comp_id[1]

                        mongo_cur4 = []
                        for block in blocks:
                            if block['block_id'] == component_id:
                                mongo_cur4.append(block)

                        # query to get the problem document with the _id.name as problem id and category as problem.
                        try:
                            p = mongo_cur4[0]
                            if p['block_type']!='library_content':

                                i = active_version
                                problem_id = 'block-v1:' + i['org'] + '+' + i['course'] + '+' + i['run'] + '+type@' + comp_id[0] + '+block@' + component_id
                                mysql_cur = db_mysql.cursor()  # Getting MySQL cursor object

                                # Query to get the grades for the student for that particular problem
                                mysql_cur.execute(problem_query, (str(student_id), str(problem_id),))  # Executing query
                                row = mysql_cur.fetchone()  # Fetching the row returned, only one row shall be returned
                                try:
                                    grade = row[0]  # Getting the grade of the student for this problem
                                    maxgrade = row[1]  # Getting the max_grade of the student for this problem
                                    try:
                                        weight_of_problem = p['fields']['weight']  # Getting the weight of the problem
                                    except:
                                        weight_of_problem=maxgrade                              #If no weight is defined, weight=maxgrade

                                    score_obt = grade * weight_of_problem / maxgrade  # Weighted score obtained for this problem
                                    tot_score = weight_of_problem  # Weighted total score for this problem
                                    sum_prob_score_obt += score_obt
                                    sum_tot_prob_score += tot_score
                                except:
                                    try:
                                        weight_of_problem=p['fields']['weight']
                                    except:
                                        weight_of_problem=0             #If weight is not defined and the problem has not been attempted
                                    sum_tot_prob_score+=weight_of_problem
                            else:
                                list3 = p['fields'][
                                    'children']  # getting the children array for this vertical, consisiting of list of component ids
                                for o in range(len(list3)):  # Iterating over the list of component ids
                                    comp_id = list3[o]  # Getting the component id
                                    component_id = comp_id[1]

                                    mongo_cur4 = []
                                    for block in blocks:
                                        if block['block_id'] == component_id:
                                            mongo_cur4.append(block)
                                    try:
                                        p = mongo_cur4[0]
                                        if p['block_type'] == 'problem':

                                            i = active_version
                                            problem_id = 'block-v1:' + i['org'] + '+' + i['course'] + '+' + i[
                                                'run'] + '+type@' + comp_id[0] + '+block@' + component_id
                                            mysql_cur = db_mysql.cursor()  # Getting MySQL cursor object

                                            # Query to get the grades for the student for that particular problem
                                            mysql_cur.execute(problem_query,
                                                              (str(student_id), str(problem_id),))  # Executing query
                                            row = mysql_cur.fetchone()  # Fetching the row returned, only one row shall be returned
                                            try:
                                                grade = row[0]  # Getting the grade of the student for this problem
                                                maxgrade = row[1]  # Getting the max_grade of the student for this problem
                                                try:
                                                    weight_of_problem = p['fields'][
                                                        'weight']  # Getting the weight of the problem
                                                except:
                                                    weight_of_problem = maxgrade  # If no weight is defined, weight=maxgrade

                                                score_obt = grade * weight_of_problem / maxgrade  # Weighted score obtained for this problem
                                                tot_score = weight_of_problem  # Weighted total score for this problem
                                                sum_prob_score_obt += score_obt
                                                sum_tot_prob_score += tot_score
                                            except:
                                                try:
                                                    weight_of_problem = p['fields']['weight']
                                                except:
                                                    weight_of_problem = 0  # If weight is not defined and the problem has not been attempted
                                                sum_tot_prob_score += weight_of_problem
                                    except:
                                        continue

                        except:
                            continue

                if sum_tot_prob_score > 0:
                    avg_score_sequential = sum_prob_score_obt / sum_tot_prob_score  # Calculating avg score of this sequential
                else:
                    avg_score_sequential = 0
                if count == 1:
                    if count_doc > 1:
                        highchart_list.append(str(short_label) + str(sequential_coun))
                    else:
                        highchart_list.append(str(short_label))
                    highchart_list2.append(str(avg_score_sequential))
                else:
                    if count_doc > 1:
                        highchart_list.append(str(short_label) + str(sequential_coun))
                    else:
                        highchart_list.append(str(short_label))
                    highchart_list2.append(str(avg_score_sequential))
                best_score_list.append(avg_score_sequential)  # Adding the sequential score to best_score_list
            best_score_list.sort(reverse=True)  # Sorting the scores list for that format in descending order
            sum_score_format = 0  # Initializing sum score of format to 0
            if sequential_coun<min_count-drop_count:
                completed = False
            for q in range(sequential_coun - drop_count):  # Getting the sum of best scores in the format
                sum_score_format += best_score_list[q]
            if sequential_coun - drop_count > 0:
                avg_score_format = sum_score_format / (
                sequential_coun - drop_count)  # Getting average score of the format
                if sequential_coun - drop_count > 1:
                    if count == 1:
                        highchart_list.append(str(short_label) + 'Avg')
                        highchart_list2.append(str(avg_score_format))
                    else:
                        highchart_list.append(str(short_label) + 'Avg')
                        highchart_list2.append(str(avg_score_format))
                stud_avg_tot += avg_score_format * weight
            else:
                avg_score_format = 0
                # Getting total student average score

        if not completed:
            highchart_list2.append(None)
        elif len(highchart_list2) > 0:
            if count == 1:
                highchart_list2.append(str(stud_avg_tot))
            else:
                highchart_list2.append(str(stud_avg_tot))
        else:
            highchart_list2 = [None, ]
    except:
    	highchart_list2=[None,]

    highchart_list3['total_score'] = highchart_list2[(len(highchart_list2)-1)]

    grade = ''

    if highchart_list3['total_score'] != None:

        prev = -1

        for grades in grade_cutoffs.keys():
            if float(highchart_list3['total_score'])>=grade_cutoffs[grades] and grade_cutoffs[grades]>prev:
                grade = grades
                prev = grade_cutoffs[grades]

        if grade=='':
            grade='Fail'

    highchart_list3['grade'] = grade

    h_list = {}

    for k in range((len(highchart_list2) - 1)):
        h_list[highchart_list[k+1]] = highchart_list2[k]

    highchart_list3['units'] = h_list

    return highchart_list3


""" Description: Function to get grading policy of a course called by get_student_course_grade()
    Input Parameters:
            course_name: name of the course for which grading policy is required
            course_run: run of the course for which grading policy is required
            course_organization: organization of the course for which grading policy is required
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


""" Description: Function to get quiz level grades of all students in all courses
    Input Parameters:
            None
    Output Type : List of all courses with a list of grades of all students enrolled in the course
    Author: Jay Goswami
    Date of creation: 17 June 2017
"""


def get_all_students_courses_grades():
    try:
        db_mysql = MySQLdb.connect(user=sql_user, passwd=sql_pswd, db=mysql_db) # Establishing MySQL connection
    except:
        print "MySQL connection not established"
        return HttpResponse("MySQL connection not established") # MySQL could not be connected

    query = "select distinct course_id from courseware_studentmodule where grade>0 and binary course_id like 'course%'"

    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(query)
    course_list = mysql_cursor.fetchall()

    courses_grade_list = []

    for course in course_list:
        course = course[0]
        course = course.split(":")[1]
        course = course.split("+")
        course_name = course[1]
        course_run = course[2]
        course_organization = course[0]
        grades = get_all_student_grades(course_name, course_run, course_organization)
        if grades:
            courses_grade_list.append(grades)
    db_mysql.close()
    return courses_grade_list


""" Description: Function to get quiz level grades of a student in all the enrolled courses
    Input Parameters:
            student_id: id of the student whose grades are required (ex. 12)
    Output Type : List of grades of the student in all enrolled courses
    Author: Jay Goswami
    Date of creation: 17 June 2017
"""


def get_all_courses_student_grades(student_id):
    try:
        db_mysql = MySQLdb.connect(user=sql_user, passwd=sql_pswd, db=mysql_db) # Establishing MySQL connection
    except:
        print "MySQL connection not established"
        return HttpResponse("MySQL connection not established") # MySQL could not be connected

    try:
        mongo_client = pymongo.MongoClient()  # Establishing MongoDB connection
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established") # MongoDB could not be connected

    query = "select username, email from auth_user where id = %s"
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(query, (str(student_id),))
    student = mysql_cursor.fetchone()

    query = "select course_id from student_courseenrollment where user_id = %s"
    problem_query = "Select grade,max_grade from courseware_studentmodule where max_grade is not null and grade is not null and student_id=%s and module_id=%s"

    mysql_cursor.execute(query, (str(student_id),))
    course_list = mysql_cursor.fetchall()

    grade_list = {}
    grade_list['name'] = student[0]
    grade_list['email'] = student[1]
    grade_list['id'] = int(student_id)

    courses_grade_list = []

    for course in course_list:
        course = course[0]
        course = course.split(":")[1]
        course = course.split("+")
        course_name = course[1]
        course_run = course[2]
        course_organization = course[0]
        dict = {}
        dict['course_name'] = course_name
        dict['course_organization'] = course_organization
        dict['course_run'] = course_run
        dict['grade'] = ''
        dict['total_score'] = 0
        dict['units'] = {}
        grading_policy = get_grading_policy(course_name, course_run, course_organization)
        try:
            grading_list = grading_policy['grader']
            grade_cutoffs = grading_policy['grade_cutoffs']
        except:
            continue
        grades = get_student_course_grades(student[1], student[0], student_id, course_name, course_run, course_organization, 1, db_mysql,mongo_client, problem_query, grading_list, grade_cutoffs)
        dict['grade'] = grades['grade']
        dict['total_score'] = grades['total_score']
        dict['units'] = grades['units']
        courses_grade_list.append(dict)

    grade_list['courses'] = courses_grade_list

    mongo_client.close()
    db_mysql.close()
    return grade_list


""" Description: Function to get quiz level grades of all students in all courses
    Input Parameters:
            None
    Output Type : List of all students with a list of grades of the student in all enrolled courses
    Author: Jay Goswami
    Date of creation: 17 June 2017
"""


def get_all_students_grades():
    try:
        db_mysql = MySQLdb.connect(user=sql_user, passwd=sql_pswd, db=mysql_db) # Establishing MySQL connection
    except:
        print "MySQL connection not established"
        return HttpResponse("MySQL connection not established") # MySQL could not be connected

    query = "select id from auth_user order by id"
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(query)
    students = mysql_cursor.fetchall()

    list = []

    for student in students:
        list.append(get_all_courses_student_grades(student[0]))

    db_mysql.close()
    return list
