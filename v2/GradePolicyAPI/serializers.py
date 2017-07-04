""" Django REST Framework Serializers """
from rest_framework import serializers


class CourseGradeSerializer(serializers.Serializer):
    """ Serializer for Courses and their grade policy """
    course_id = serializers.CharField()
    course_display_name = serializers.CharField()
    organization = serializers.CharField()
    run = serializers.CharField()
    name = serializers.CharField()
    course_start = serializers.DateField(allow_null=True)
    course_end = serializers.DateField(allow_null=True)
    course_registration_start = serializers.DateField(allow_null=True)
    course_registration_end = serializers.DateField(allow_null=True)
    grader = serializers.ListField(allow_null=True)
    grade_cutoffs = serializers.DictField(allow_null=True)