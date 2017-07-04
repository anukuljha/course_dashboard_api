""" Django REST Framework Serializers """
from rest_framework import serializers


class StudentDiscussionSerializer(serializers.Serializer):
    """ Serializer for Student Discussion Count """
    user_id = serializers.IntegerField()
    count = serializers.DictField(allow_null=True)


class CourseDiscussionSerializer(serializers.Serializer):
    """ Serializer for Student Discussion Count """
    course_id = serializers.CharField()
    count = serializers.DictField(allow_null=True)
