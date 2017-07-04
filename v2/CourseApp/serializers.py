from rest_framework import serializers
from models import AuthUser,StudentCourseAccessrole
import MySQLdb
from course_dashboard_api.v2.dbv import *
class CourseSummarySerializer(serializers.Serializer):
    course_id = serializers.CharField()
    course_display_name = serializers.CharField(allow_null=True)
    course_start = serializers.DateTimeField(allow_null=True)
    course_end = serializers.DateTimeField(allow_null=True)
    course_registration_start = serializers.DateTimeField(allow_null=True)
    course_registration_end = serializers.DateTimeField(allow_null=True)
    course_status = serializers.CharField(allow_null=True)
    course_team = serializers.DictField(allow_null=True)
    course_student_count = serializers.CharField(allow_null=True) #<- Last Edit

class CourseDetailsSerializer(serializers.Serializer):
    course_id = serializers.CharField()
    course_display_name = serializers.CharField(allow_null=True)
    course_start = serializers.DateTimeField(allow_null=True)
    course_end = serializers.DateTimeField(allow_null=True)
    course_registration_start = serializers.DateTimeField(allow_null=True)
    course_registration_end = serializers.DateTimeField(allow_null=True)
    course_status = serializers.CharField(allow_null=True)
    course_team = serializers.DictField(allow_null=True)
    course_student_count = serializers.CharField(allow_null=True) #<- Last Edit
    course_grading_policy = serializers.DictField(allow_null=True)

class FacultyCourseDetailsSerializer(serializers.Serializer):

    faculty_id = serializers.IntegerField()
    faculty_email = serializers.EmailField()
    faculty_username = serializers.CharField()
    faculty_course_list = CourseDetailsSerializer(many=True)

class FacultyCourseSummarySerializer(serializers.Serializer):

    faculty_id = serializers.IntegerField()
    faculty_email = serializers.EmailField()
    faculty_username = serializers.CharField()
    faculty_course_list = CourseSummarySerializer(many=True)

class CustomRoleInfoSerializer(serializers.Serializer):
    course_id = serializers.CharField(allow_null=False)
    course_instructors = serializers.ListField(allow_null=False)
    course_members = serializers.ListField(allow_null=False)

class PostCustomRoleSerializer(serializers.Serializer):

    course_org    = serializers.CharField(write_only=True)
    course_number = serializers.CharField(write_only=True)
    course_run    = serializers.CharField(write_only=True)
    org           = serializers.CharField(read_only =True)

    #course_id = serializers.CharField(allow_null=False)

    role = serializers.CharField()

    email_id = serializers.EmailField(write_only=True)

    def validate(self, data):
        import re
        pattern = re.compile(r'[A-Za-z0-9._-]+$')
        if not pattern.match(data['course_org']):
            raise serializers.ValidationError('Course Org should only have alphanumerics,(.),(-),(_)')
        if not pattern.match(data['course_number']):
            raise serializers.ValidationError('Course Number should only have alphanumerics,(.),(-),(_)')
        if not pattern.match(data['course_run']):
            raise serializers.ValidationError('Course Run should only have alphanumerics,(.),(-),(_)')
        pattern1 = re.compile(r'(staff|instructor|beta_testers)$')
        if not pattern1.match(data['role']):
            raise serializers.ValidationError('Course Role can be `instructor` OR `staff` OR `beta_testers`')
        return data
    def create(self, validated_data):
        sql_user = MYSQL_USER
        sql_pswd = MYSQL_PSWD
        sql_db = MYSQL_DB
        try:
            db_mysql = MySQLdb.connect(user=sql_user, passwd=sql_pswd, db=sql_db)  # Establishing MySQL connection
        except:
            raise serializers.DjangoValidationError("MySQL connection not established")

        mcourse_id = 'course-v1:'+validated_data['course_org']+'+'+validated_data['course_number']+'+'+validated_data['course_run']
        morg = validated_data['course_org']
        mid = self.context['request'].user.id
        memailid = validated_data['email_id']
        # print mid
        instuctor_query = "select count(*) from student_courseaccessrole where role = 'instructor' " \
                          "AND BINARY course_id = %s AND BINARY user_id = %s AND BINARY org = %s   "
        user_query      =""
        mysql_cursor = db_mysql.cursor()

        mysql_cursor.execute(instuctor_query, (mcourse_id, mid, morg))

        boolAccess = mysql_cursor.fetchall()[0][0];

        # print boolAccess
        if boolAccess == 0:
            raise serializers.ValidationError("You dont have permission to do that")
        else:
            muser = AuthUser.objects.get(email=memailid)
            print muser.id
            print mcourse_id
            role = StudentCourseAccessrole(
                org=validated_data['course_org'],
                course_id=mcourse_id,
                role=validated_data['role'],
                user=muser
            )
            role.save()
            return role
            '''try:
                muser = AuthUser.objects.get(email=memailid)
                print muser.id
                print mcourse_id
                role = StudentCourseAccessrole(
                    org=validated_data['course_org'],
                    course_id=mcourse_id,
                    role=validated_data['role'],
                    user=muser
                )
                role.save()
                return role
            except:
                raise serializers.ValidationError("Multiple Entries not allowed!")'''

class CourseCohortSerializer(serializers.Serializer):

    cohort_id = serializers.IntegerField()
    cohort_name = serializers.CharField()
    cohort_student_list = serializers.ListField()
    cohort_type = serializers.CharField()

class AllCourseCohortSerializer(serializers.Serializer):

    course_id = serializers.CharField()

    course_cohorts_list = CourseCohortSerializer(many=True)
