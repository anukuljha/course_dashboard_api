"""
Course API URI specification.
"""
from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    '',

    url(r'^', include('course_dashboard_api.v2.GradePolicyAPI.urls')),
    url(r'^', include('course_dashboard_api.v2.GradeAPI.urls')),
    url(r'^', include('course_dashboard_api.v2.DiscussionAPI.urls')),
    url(r'^', include('course_dashboard_api.v2.CourseStructureAPI.urls')),
    url(r'^', include('course_dashboard_api.v2.CourseAPI.urls')),
    url(r'^', include('course_dashboard_api.v2.CourseApp.urls')),
)
