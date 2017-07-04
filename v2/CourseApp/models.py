# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class StudentCourseAccessrole(models.Model):
    org = models.CharField(max_length=64)
    course_id = models.CharField(max_length=255)
    role = models.CharField(max_length=64)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'student_courseaccessrole'
        unique_together = (('user', 'org', 'course_id', 'role'),)
