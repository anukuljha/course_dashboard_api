from rest_framework import generics
from api import *
from serializers import CourseStudentSerializer, StudentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication
from permissions import IsStudent, IsFaculty

# Create your views here.


class CourseGradeList(generics.ListAPIView):
    """
        **Use Case**
            
            *Get a paginated list of courses with all its students and their grades in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/courses/v2/grades/courses/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.
              
                * course_name: Name of the course
              
                * course_organization: The organization specified for the course.
                
                * course_run: The run of the course.
                
                * students: 

                    * id: The unique identifier for the student.

                    * name: Name of the student
                    
                    * email: Email of the student
                    
                    * grade: Overall grade of the student in the course
                    
                    * total_score: Total score of the student in the course
                    
                    * units: List of grades of individual units of the student

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """

    queryset = get_all_students_courses_grades()
    serializer_class = CourseStudentSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class CourseGradeDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get all the students and their grades for a specific course.

        **Example Requests**

              GET /api/courses/v2/grades/courses/{course_organization}+{course_name}+{course_run}

        **Response Values**

            On success with Response Code <200>

            * course_name: Name of the course
              
            * course_organization: The organization specified for the course.
                
            * course_run: The run of the course.
                
            * students: 

                * id: The unique identifier for the student.

                * name: Name of the student
                    
                * email: Email of the student
                    
                * grade: Overall grade of the student in the course
                
                * total_score: Total score of the student in the course
                    
                * units: List of grades of individual units of the student

         **ERROR RESPONSES**

                * Response Code <404> COURSE NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = CourseStudentSerializer
    permission_classes = (IsAdminUser, IsFaculty)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            list = get_all_student_grades(self.kwargs['name'], self.kwargs['run'], self.kwargs['org'])
            list['course_name']
            return list
        except:
            raise Http404


class StudentList(generics.ListCreateAPIView):
    """
        **Use Case**
 
            *Get a paginated list of students with all their courses and the grades in the edX Platform.

                Each page in the list can contain up to 10 students.

        **Example Requests**

              GET /api/courses/v2/grades/students/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * id: The unique identifier for the student.

                * name: Name of the student
                    
                * email: Email of the student

                * courses:
                
                    * course_name: Name of the course
              
                    * course_organization: The organization specified for the course.
                
                    * course_run: The run of the course.

                    * grade: Overall grade of the student in the course
                    
                    * total_score: Total score of the student in the course
                    
                    * units: List of grades of individual units of the student

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """
    queryset = get_all_students_grades()
    serializer_class = StudentSerializer
    http_method_names = ['get']
    permission_classes = (IsAdminUser,)
    # authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class StudentGradeDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get all the courses and the grades for a specific student.

        **Example Requests**

              GET /api/courses/v2/grades/students/{student_id}

        **Response Values**

            On success with Response Code <200>

            * id: The unique identifier for the student.

            * name: Name of the student
                    
            * email: Email of the student

            * courses:
                
                * course_name: Name of the course
              
                * course_organization: The organization specified for the course.
                
                * course_run: The run of the course.

                * grade: Overall grade of the student in the course
                
                * total_score: Total score of the student in the course
                
                * units: List of grades of individual units of the student

         **ERROR RESPONSES**

                * Response Code <404> STUDENT NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = StudentSerializer
    permission_classes = (IsAdminUser, IsStudent)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            student_id = self.kwargs['student_id']
            list = get_all_courses_student_grades(student_id)
            list['id']
            return list
        except:
            raise Http404