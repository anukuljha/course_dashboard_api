"""
Course API v1 URL specification
"""
from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',

    url(r'^certificates/count/$', views.CourseCertificateList.as_view()),
    url(r'^certificates/count/(?P<org>[A-Za-z0-9_.-]+)[+](?P<name>[A-Za-z0-9_.-]+)[+](?P<run>[A-Za-z0-9_.-]+)/$', views.CourseCertificateDetail.as_view()),
    url(r'^certificates/detail/$', views.CourseStudentCertificateList.as_view()),
    url(r'^certificates/detail/(?P<org>[A-Za-z0-9_.-]+)[+](?P<name>[A-Za-z0-9_.-]+)[+](?P<run>[A-Za-z0-9_.-]+)/$', views.CourseStudentCertificateDetail.as_view()),
    url(r'^detail/$', views.CourseGradeList.as_view()),
    url(r'^detail/(?P<org>[A-Za-z0-9_.-]+)[+](?P<name>[A-Za-z0-9_.-]+)[+](?P<run>[A-Za-z0-9_.-]+)/$', views.CourseGradeDetail.as_view()),
    url(r'^courses/$', views.CourseList.as_view()),
)