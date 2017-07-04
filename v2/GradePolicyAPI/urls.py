"""
Course Grade Policy API v1 URL specification
"""
from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',

    url(r'^grading_policies/$', views.CourseGradeList.as_view()),
    url(r'^grading_policies/(?P<org>[A-Za-z0-9_.-]+)[+](?P<name>[A-Za-z0-9_.-]+)[+](?P<run>[A-Za-z0-9_.-]+)/$', views.CourseGradeDetail.as_view()),
)