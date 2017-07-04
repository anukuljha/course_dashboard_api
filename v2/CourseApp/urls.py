from django.conf.urls import url
import views

from serializers import *

urlpatterns = [

    url(r'^status/(?P<status>(all|upcoming|ongoing|archived))/$', views.StatusCoursesList.as_view(), ),
    url(r'^status/details/(?P<status>(all|upcoming|ongoing|archived))/$', views.StatusCoursesList.as_view(serializer_class = CourseDetailsSerializer), ),

    url(r'^faculties/summary/$', views.FacultyCoursesList.as_view(),),
    url(r'^faculties/summary/(?P<faculty>[A-Za-z0-9_-]+)/$',views.FacultyCourseInstance.as_view()),
    url(r'^faculties/details/$',views.FacultyCoursesList.as_view(serializer_class = FacultyCourseDetailsSerializer)),
    url(r'^faculties/details/(?P<faculty>[A-Za-z0-9_-]+)/$',views.FacultyCourseInstance.as_view(serializer_class = FacultyCourseDetailsSerializer)),

    url(r'^cohorts/$', views.CoursesCohortsList.as_view() ),
    url(r'^cohorts/(?P<courseid>[A-Za-z0-9+._-]+)/$', views.CourseCohortsInstance.as_view() ),

    url(r'^roles/$',views.CoursesTeamList.as_view()),
]
