from rest_framework import generics
from api import *
from serializers import StudentDiscussionSerializer, CourseDiscussionSerializer
from rest_framework.permissions import IsAdminUser
from django.http import Http404
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication
from permissions import IsStudent, IsFaculty

# Create your views here.


class StudentDiscussionList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of students with their count of discussions and questions in the edX Platform.

                Each page in the list can contain up to 10 students.

        **Example Requests**

              GET /api/courses/v2/discussions/students/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * user_id: The unique identifier for the student.

                * count:

                    * discussion: Count of discussions by the student

                    * question: Count of questions asked by the student

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """

    queryset = get_all_students_count()
    serializer_class = StudentDiscussionSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class StudentDiscussionDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get count of discussions and questions for a specific student.

        **Example Requests**

              GET /api/courses/v2/discussions/students/{student_id}

        **Response Values**

            On success with Response Code <200>

            * user_id: The unique identifier for the student.

                * count:

                    * discussion: Count of discussions by the student

                    * question: Count of questions asked by the student

         **ERROR RESPONSES**

                * Response Code <404> STUDENT NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = StudentDiscussionSerializer
    permission_classes = (IsAdminUser, IsStudent, )
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            student_id = self.kwargs['student_id']
            list = get_count_student(student_id)
            list['user_id']
            return list
        except:
            raise Http404


class CourseDiscussionList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of courses with their count of discussions and questions in the edX Platform.

                Each page in the list can contain up to 10 students.

        **Example Requests**

              GET /api/courses/v2/discussions/courses/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * course_id: The unique identifier for the course.

                * count:

                    * discussion: Count of discussions by the course

                    * question: Count of questions asked by the course

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """

    queryset = get_all_courses_count()
    serializer_class = CourseDiscussionSerializer
    permission_classes = (IsAdminUser, )
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class CourseDiscussionDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get count of discussions and questions for a specific course.

        **Example Requests**

              GET /api/courses/v2/discussions/courses/{course_id}

        **Response Values**

            On success with Response Code <200>

            * course_id: The unique identifier for the course.

                * count:

                    * discussion: Count of discussions by the course

                    * question: Count of questions asked by the course

         **ERROR RESPONSES**

                * Response Code <404> COURSE NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = CourseDiscussionSerializer
    permission_classes = (IsAdminUser, IsFaculty, )
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            course_id = self.kwargs['course_id']
            list = get_count_course(course_id)
            list['course_id']
            return list
        except:
            raise Http404