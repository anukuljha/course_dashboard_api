# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from rest_framework import permissions,generics
from rest_framework.throttling import UserRateThrottle
from serializers import *
from CourseApiData import *
from django.http import Http404

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication

class MyUserThrottle(UserRateThrottle):

    rate = '40/minute'

    def allow_request(self, request, view):
        return super(MyUserThrottle, self).allow_request(request, view)


class StatusCoursesList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of courses available on edX platform based on Course Run.

                The list can be filtered based on status.
                STATUS = `all` |` ongoing` | `upcoming` | `archived`

                Each page in the list can contain up to 10 courses.


        **Example Requests**

              GET /api/courses/v2/status/{`all`|`archived`|`ongoing`|`upcoming`}
              
              GET /api/courses/v2/status/details/{`all`|`archived`|`ongoing`|`upcoming`}

              

        **GET Response Values**
        
            On success with Response Code <200>

            * count: The number of Courses having status {all|ongoing|upcoming|archived} in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:
                A list of Courses returned. Each collection in the list
                contains these fields.
                
                * course_id                 :Id of the course.
                * course_display_name       :Display name of the course.
                * course_start              :Course start date and time.
                * course_end                :Course end date and time.
                * course_registration_start :Course registration start date and time.
                * course_registration_end   :Course registration end date and time.
                * course_status             :Running status of course.
                * course_team               :Course Team
                    * course_instructors    :List of course instructors.
                        * username          :Username of Course Instructor.
                        * email             :EmailId of Course Instructor.
                    * course_members        :List of course members.
                        * username          :Username of Course Member.
                        * email             :EmailId of Course Member.
                * course_student_count      :Count of students enrolled in the course.

                With  (/details/)

                * course_grading_policy     :
                    * grader        :   List of different assignments type and their details like total number, weight, number of droppable.
                    * grade_cutoffs :   List of different grades of the course, with their individual range.


            **ERROR RESPONSES**

                * Response Code <404> NOT FOUND
                * Response Code <403> FORBIDDEN
                * Response Code <>

    """

    http_method_names = ['get']
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CourseSummarySerializer
    throttle_classes = (MyUserThrottle,)

    def get_queryset(self):

        return get_courses_with_status(self.kwargs['status'],True)


class FacultyCoursesList(generics.ListAPIView):
    """
        **Use Case**

            * Get a paginated list of courses available on edX platform under given 
              faculty name OR all faculties.

                The list can be filtered based on faculty name.

                Each page in the list can contain up to 10 courses.


        **Example Requests**

              GET /api/courses/v2/faculties/summary/
                  
              GET /api/courses/v2/faculties/summary/{faculty name}

              GET /api/courses/v2/faculties/details/
                  
              GET /api/courses/v2/faculties/details/{faculty name}
                  
              Note : If Faculty name is not provided a list is obtained in 
                     which courses are grouped based on faculty.
                     If Faculty name is provided a single instance is obtained 
                     with the list of courses under that faculty.This response will not be paginated.


        **GET Response Values**

            On success with Response Code <200>

            * count: The number of Courses under given faculty in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:
                A list is returned. Each collection in the list
                contains these fields.
                * faculty_id        :
                * faculty_email     :
                * faculty_username  :
                * faculty_course_list   :
                            
                    * course_id                 :Id of the course.
                    * course_display_name       :Display name of the course.
                    * course_start              :Course start date and time.
                    * course_end                :Course end date and time.
                    * course_registration_start :Course registration start date and time.
                    * course_registration_end   :Course registration end date and time.
                    * course_status             :Running status of course.
                    * course_team               :Course Team
                        * course_instructors    :List of course instructors.
                            * username          :Username of Course Instructor.
                            * email             :EmailId of Course Instructor.
                        * course_members        :List of course members.
                            * username          :Username of Course Member.
                            * email             :EmailId of Course Member.
                    * course_student_count      :Count of students enrolled in the course.
    
                    With  (/details/)
    
                    * course_grading_policy     :
                        * grader        :   List of different assignments type and their details 
                                            like total number, weight, number of allowed drops.
                        * grade_cutoffs :   List of different grades of the course, with their individual range.




            **ERROR RESPONSES**

                * Response Code <404> NOT FOUND
                * Response Code <403> FORBIDDEN
                * Response Code <>

    """

    http_method_names = ['get']
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FacultyCourseSummarySerializer
    throttle_classes = (MyUserThrottle,)
    def get_queryset(self):

        try :
            p = get_summary_facultywise(True)
            if p == [] or None:
                raise Http404(u"Empty list and '%s.allow_empty' is False."
                              % self.__class__.__name__)
            return p
        except :
            raise Http404(u"Empty list and '%s.allow_empty' is False."
                              % self.__class__.__name__)


class FacultyCourseInstance(generics.RetrieveAPIView):
    """
        **Use Case**

            * Get a paginated list of courses available on edX platform under given 
              faculty name OR all faculties.

                The list can be filtered based on faculty name.

                Each page in the list can contain up to 10 courses.


        **Example Requests**

              GET /api/courses/v2/faculties/summary/
                  
              GET /api/courses/v2/faculties/summary/{faculty name}

              GET /api/courses/v2/faculties/details/
                  
              GET /api/courses/v2/faculties/details/{faculty name}
                  
              Note : If Faculty name is not provided a list is obtained in 
                     which courses are grouped based on faculty.
                     If Faculty name is provided a single instance is obtained 
                     with the list of courses under that faculty.This response will not be paginated.


        **GET Response Values**

            On success with Response Code <200>

            * count: The number of Courses under given faculty in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:
                A list is returned. Each collection in the list
                contains these fields.
                * faculty_id        :
                * faculty_email     :
                * faculty_username  :
                * faculty_course_list   :
                            
                    * course_id                 :Id of the course.
                    * course_display_name       :Display name of the course.
                    * course_start              :Course start date and time.
                    * course_end                :Course end date and time.
                    * course_registration_start :Course registration start date and time.
                    * course_registration_end   :Course registration end date and time.
                    * course_status             :Running status of course.
                    * course_team               :Course Team
                        * course_instructors    :List of course instructors.
                            * username          :Username of Course Instructor.
                            * email             :EmailId of Course Instructor.
                        * course_members        :List of course members.
                            * username          :Username of Course Member.
                            * email             :EmailId of Course Member.
                    * course_student_count      :Count of students enrolled in the course.
    
                    With  (/details/)
    
                    * course_grading_policy     :
                        * grader        :   List of different assignments type and their details like 
                                            total number, weight, number of allowed drops .
                        * grade_cutoffs :   List of different grades of the course, with their individual range.




            **ERROR RESPONSES**

                * Response Code <404> NOT FOUND
                * Response Code <403> FORBIDDEN
                * Response Code <>

    """
    http_method_names = ['get']
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FacultyCourseSummarySerializer
    throttle_classes = (MyUserThrottle,)
    def get_object(self):
        try:
            p = get_summary_by_faculty_name(self.kwargs['faculty'], True)
            if p == [] or None:
                raise Http404(u"Empty list and '%s.allow_empty' is False."
                              % self.__class__.__name__)
            return p[0]
        except:
            raise Http404(u"Empty list and '%s.allow_empty' is False."
                          % self.__class__.__name__)


class CoursesTeamList(generics.ListCreateAPIView):

    """
       **Use Case**

           *Get a paginated list of teams of each course present in edX platform for which 
            the logged in user is a faculty.
            
            If the logged in user is not a faculty in any of the courses an empty list is obtained.

            Each page in the list can contain up to 10 entries.

       **Example Requests**

             GET /api/courses/v2/role/

             POST /api/courses/v2/role/ 
            {
                "course_org": "IITBombayX",
                "course_number": "PRC101",
                "course_run": "2017",
                "role": "instructor",
                "email_id": "audit@example.com"
            }

       ** Post Parameters ** 
       
            A POST request must have following prameters
            
            course_org    : Organization of Course(Only Alphanumerics and (.),(-),(_) allowed not other special characters allowed).
            course_number : Course Number (Only Alphanumerics and (.),(-),(_) allowed not other special characters allowed).
            course_run    : Course Run (Only Alphanumerics and (.),(-),(_) allowed not other special characters allowed).
            role          : Members role (Only 'instructor' OR 'staff' OR 'beta testers'),
            email_id      : Valid Email Id of user to which the above role is assigned.

       **GET Response Values**
           On success with Response Code <200>

           * count: The number of Users registered in the edX platform.

           * next: The URI to the next page of courses.

           * previous: The URI to the previous page of courses.

           * num_pages: The number of pages listing courses.

           * results:
               A list of teams present in each course belonging to the logged in faculty.
                Each item in list contains following values:
               * course_id: The unique identifier for the user.

               * course_instructors: List of email id of faculties in that course.

               * course_members: List of email id of members in that course.

           **ERROR RESPONSES**

               * Response Code <404> NOT FOUND
               * Response Code <403> FORBIDDEN
               * Response Code <>


       **POST Response Value**

           On success with Response Code <200>

           Following details of successfully registered user are obtained

           * org : Organization of the course that particular user is assigned to. 
           * role: Role which that user is assigned. 

           ** ERROR RESPONSES**

               * Response Code <404> NOT FOUND
               * Response Code <403> FORBIDDEN
               * Response Code <>

    """

    http_method_names = ['get','post']
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated,)
    throttle_classes = (MyUserThrottle,)
    def get_queryset(self):
        return get_all_course_teams(self.request.user.id)
    def get_serializer_class(self):

        if self.request.method == 'GET' :
            return CustomRoleInfoSerializer
        if self.request.method == 'POST' :
            return PostCustomRoleSerializer


class CoursesCohortsList(generics.ListAPIView):
    """
        **Use Case**

            * Get a paginated list of cohorts available on edX platform.

                The list can be filtered based on course id.

                Each page in the list can contain up to 10 courses.


        **Example Requests**

              GET /api/courses/v2/cohorts/

              GET /api/courses/v2/cohorts/{course id}

              Note : * If Course id is not provided a list is obtained in 
                       which cohorts are grouped based on course id.
                     * If Course id is provided this will give a single json instance which includes the list of 
                       all cohorts in that particular course.
                     * If that course is not present or there are no cohorts in that course Response 404 NOT FOUND 
                       is obtained
 

        **GET Response Values**

            On success with Response Code <200>

            * count: The number of Courses in the edX platform which has courses.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:
                A list is returned. Each collection in the list
                contains these fields.
                * course_id : Id of the course.
                * course_cohorts_list : List of cohorts present in that course
                    * cohort_id             : Id of the cohort.
                    * cohort_name           : Name of the cohort.
                    * cohort_student_list   : List of students present in that cohort.
                        * id                : id of student.
                        * username          : username of student.
                    * cohort_type           : Type of the cohort 

            **ERROR RESPONSES**

                * Response Code <404> NOT FOUND
                * Response Code <403> FORBIDDEN
                * Response Code <>

    """

    http_method_names = ['get']
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AllCourseCohortSerializer
    throttle_classes = (MyUserThrottle,)
    def get_queryset(self):

        try :
            p = get_all_courses_cohorts()
            if p == [] or None:
                raise Http404(u"Empty list and '%s.allow_empty' is False."
                              % self.__class__.__name__)
            return p
        except :
            raise Http404(u"Empty list and '%s.allow_empty' is False."
                              % self.__class__.__name__)


class CourseCohortsInstance(generics.RetrieveAPIView):
    """
            **Use Case**

                * Get a paginated list of cohorts available on edX platform.

                    The list can be filtered based on course id.

                    Each page in the list can contain up to 10 courses.


            **Example Requests**

                  GET /api/courses/v2/cohorts/

                  GET /api/courses/v2/cohorts/{course id}

                  Note : * If Course id is not provided a list is obtained in 
                           which cohorts are grouped based on course id.
                         * If Course id is provided this will give a single json instance which includes the list of 
                           all cohorts in that particular course.
                         * If that course is not present or there are no cohorts in that course Response 404 NOT FOUND 
                           is obtained


            **GET Response Values**

                On success with Response Code <200>

                * count: The number of Courses in the edX platform which has courses.

                * next: The URI to the next page of courses.

                * previous: The URI to the previous page of courses.

                * num_pages: The number of pages listing courses.

                * results:
                    A list is returned. Each collection in the list
                    contains these fields.
                    * course_id : Id of the course.
                    * course_cohorts_list : List of cohorts present in that course
                        * cohort_id             : Id of the cohort.
                        * cohort_name           : Name of the cohort.
                        * cohort_student_list   : List of students present in that cohort.
                            * id                : id of student.
                            * username          : username of student.
                        * cohort_type           : Type of the cohort 

                **ERROR RESPONSES**

                    * Response Code <404> NOT FOUND
                    * Response Code <403> FORBIDDEN
                    * Response Code <>

        """

    http_method_names = ['get']
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CourseCohortSerializer
    throttle_classes = (MyUserThrottle,)
    def get_object(self):
        try:
            mcourse_id = 'course-v1:' + self.kwargs['courseid']
            p = get_course_cohort_details(mcourse_id)
            return p[0]
        except:
            raise Http404(u"Empty list and '%s.allow_empty' is False."
                          % self.__class__.__name__)
