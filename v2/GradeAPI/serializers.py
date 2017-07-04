""" Django REST Framework Serializers """
from rest_framework import serializers


class StudentGradeSerializer(serializers.Serializer):
    """ Serializer for Student with all grades in individual units """
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    total_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    units = serializers.DictField(allow_null=True)
    grade = serializers.CharField(allow_null=True)


class CourseStudentSerializer(serializers.Serializer):
    """ Serializer for Course with all its students and their grades """
    course_name = serializers.CharField()
    course_organization = serializers.CharField()
    course_run = serializers.CharField()
    students = StudentGradeSerializer(many=True)


class CourseGradeSerializer(serializers.Serializer):
    """ Serializer for Course and student's grades in the course """
    course_name = serializers.CharField()
    course_organization = serializers.CharField()
    course_run = serializers.CharField()
    total_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    units = serializers.DictField(allow_null=True)
    grade = serializers.CharField(allow_null=True)


class StudentSerializer(serializers.Serializer):
    """ Serializer for Student with all its courses and their grades """
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    courses = CourseGradeSerializer(many=True, allow_null=True)