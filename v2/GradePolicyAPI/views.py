""" API implementation for course grade-policy """

from rest_framework import generics
from api import *
from serializers import CourseGradeSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication

# Create your views here.


class CourseGradeList(generics.ListAPIView):
    """
        **Use Case**
        
            *Get a paginated list of courses with their grading policies in the edX Platform.
                
                Each page in the list can contain up to 10 courses.
                
        **Example Requests**
        
              GET /api/courses/v2/grading_policies
              
        **Response Values**
        
            On success with Response Code <200>
        
            * count: The number of courses in the edX platform.
            
            * next: The URI to the next page of courses.
            
            * previous: The URI to the previous page of courses.
            
            * num_pages: The number of pages listing courses.
            
            * results:  A list of courses returned. Each collection in the list
              contains these fields.
              
                * course_id: The unique identifier for the course.
                
                * course_display_name: The display name of the course.
                
                * organization: The organization specified for the course.
                
                * run: The run of the course.
                
                * course: The course number.
                
                * course_start: The course start date.
                
                * course_end: The course end date. If course end date is not specified, the
                  value is null.
                  
                * course_registration_start: The course registration start date.
                
                * course_registration_end: The course registration end date. If course registration end date is not 
                  specified, the value is null.
                  
                * grader : List of different assignments type and their details like total number, weight, number of droppable
                
                * grade_cutoffs : List of different grades of the course, with their individual range
                
         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """
    queryset = get_all_courses_grading_policy()  # Get grading policy for all courses
    serializer_class = CourseGradeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class CourseGradeDetail(generics.RetrieveAPIView):
    """
        **Use Case**
        
            Get grade policy for a specific course.

        **Example Requests**

              GET /api/courses/v2/grading_policies{course_organization}+{course_name}+{course_run}

        **Response Values**

            On success with Response Code <200>

            * course_id: The unique identifier for the course.

            * course_display_name: The display name of the course.

            * organization: The organization specified for the course.

            * run: The run of the course.

            * name: The course name

            * course_start: The course start date.

            * course_end: The course end date. If course end date is not specified, the
                value is null.

            * course_registration_start: The course registration start date.

            * course_registration_end: The course registration end date. If course registration end date is not 
                specified, the value is null.

            * grader : List of different assignments type and their details like total number, weight, number of droppable

            * grade_cutoffs : List of different grades of the course, with their individual range

         **ERROR RESPONSES**

                * Response Code <404> COURSE NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = CourseGradeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            list = get_grading_policy(self.kwargs['name'], self.kwargs['run'], self.kwargs['org'])
            list['course_id']
            return list
        except:
            raise Http404