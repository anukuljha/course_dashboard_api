"""
Course Structure API v1 URL specification
"""
from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',

    url(r'^structures/$', views.CourseStructureList.as_view()),
    url(r'^structures/(?P<org>[A-Za-z0-9_.-]+)[+](?P<name>[A-Za-z0-9_.-]+)[+](?P<run>[A-Za-z0-9_.-]+)/$', views.CourseStructureDetail.as_view()),
)