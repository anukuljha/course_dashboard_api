"""
Grade API v1 URL specification
"""
from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',

    url(r'^grades/courses/$', views.CourseGradeList.as_view()),
    url(r'^grades/courses/(?P<org>[A-Za-z0-9_.-]+)[+](?P<name>[A-Za-z0-9_.-]+)[+](?P<run>[A-Za-z0-9_.-]+)/$', views.CourseGradeDetail.as_view()),
    url(r'^grades/students/$', views.StudentList.as_view()),
    url(r'^grades/students/(?P<student_id>[0-9]+)/$', views.StudentGradeDetail.as_view()),
)