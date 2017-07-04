"""
Permissions classes for Course-API views.
"""
from rest_framework import permissions
from django.http import HttpResponse
import MySQLdb
from course_dashboard_api.v2.dbv import *

sql_user = MYSQL_USER
sql_pswd = MYSQL_PSWD
mysql_db = MYSQL_DB


class IsFaculty(permissions.BasePermission):
    """
    Grants access if the requesting user is the faculty of the requested course or if the requesting user is a superuser.
    """
    def has_permission(self, request, view):
        try:
            db_mysql = MySQLdb.connect(user=sql_user, passwd=sql_pswd, db=mysql_db)  # Establishing MySQL connection
        except:
            print "MySQL connection not established"
            return HttpResponse("MySQL connection not established")  # MySQL could not be connected

        query = "select * from student_courseaccessrole where binary course_id = %s and role = 'instructor' and  user_id=%s"

        list = request.META['PATH_INFO'].split("/")
        id = list[len(list) - 2]
        course_id = "course-v1:" + id

        user_id = request.user.id

        mysql_cursor = db_mysql.cursor()
        mysql_cursor.execute(query, (str(course_id), str(user_id), ))
        entry = mysql_cursor.fetchone()

        permission = True

        if entry is None:
            permission = False

        return request.user.is_superuser or permission