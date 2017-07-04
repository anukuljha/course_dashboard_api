"""
Discussion API v1 URL specification
"""
from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',

    url(r'^discussions/students/$', views.StudentDiscussionList.as_view()),
    url(r'^discussions/students/(?P<student_id>[0-9]+)/$', views.StudentDiscussionDetail.as_view()),
    url(r'^discussions/courses/$', views.CourseDiscussionList.as_view()),
    url(r'^discussions/courses/(?P<course_id>[A-Za-z0-9:+_.-]+)/$', views.CourseDiscussionDetail.as_view()),
)
