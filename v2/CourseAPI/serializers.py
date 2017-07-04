""" Django REST Framework Serializers """
from rest_framework import serializers


class CourseSerializer(serializers.Serializer):
    """ Serializer for Course IDs """
    course_id = serializers.CharField()


class CourseCertificateSerializer(serializers.Serializer):
    """ Serializer for Courses with their count of certificates """
    course_id = serializers.CharField()
    name = serializers.CharField()
    run = serializers.CharField()
    organization = serializers.CharField()
    certificate_count = serializers.IntegerField()


class StudentCertificateSerializer(serializers.Serializer):
    """ Serializer for Student getting certificates """
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    grade_score = serializers.DecimalField(max_digits=5, decimal_places=2)


class CourseStudentCertificateSerializer(serializers.Serializer):
    """ Serializer for Courses with the students getting certificate """
    course_id = serializers.CharField()
    name = serializers.CharField()
    run = serializers.CharField()
    organization = serializers.CharField()
    certificate_students = StudentCertificateSerializer(many=True, allow_null=True)


class StudentSerializer(serializers.Serializer):
    """ Serializer for Student """
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    total_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    grade = serializers.CharField(allow_null=True)
    is_active = serializers.IntegerField()
    last_login = serializers.DateTimeField()


class CourseGradeSerializer(serializers.Serializer):
    """ Serializer for Course with all its students and their grades """
    course_name = serializers.CharField()
    course_organization = serializers.CharField()
    course_run = serializers.CharField()
    students = StudentSerializer(many=True, allow_null=True)