""" Django REST Framework Serializers """
from rest_framework import serializers


class UnitSerializer(serializers.Serializer):
    """ Serializer for Unit """
    name = serializers.CharField()


class SubsectionSerializer(serializers.Serializer):
    """ Serializer for SubSection """
    name = serializers.CharField()
    unit = UnitSerializer(many=True, allow_null=True)


class SectionSerializer(serializers.Serializer):
    """ Serializer for Section """
    name = serializers.CharField()
    subsection = SubsectionSerializer(many=True, allow_null=True)


class CourseStructureSerializer(serializers.Serializer):
    """ Serializer for Course Structure """
    course_id = serializers.CharField()
    section = SectionSerializer(many=True, allow_null=True)