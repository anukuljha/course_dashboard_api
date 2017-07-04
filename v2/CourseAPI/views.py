from rest_framework import generics
from api import *
from serializers import CourseCertificateSerializer, CourseSerializer, CourseGradeSerializer, CourseStudentCertificateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication
from permissions import IsFaculty
from rest_framework.throttling import UserRateThrottle

# Create your views here.


class UserThrottle(UserRateThrottle):

    rate = '40/minute'

    def allow_request(self, request, view):
        return super(UserThrottle, self).allow_request(request, view)


class CourseCertificateList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of courses with their count of certificates in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/courses/v2/certificates/count/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * course_id: The unique identifier for the course.

                * name: The course name

                * organization: The organization specified for the course.

                * run: The run of the course.

                * certificate_count: Count of certificates for the course

         **ERROR RESPONSES**

                * Response Code <404> COURSE NOT FOUND
                * Response Code <403> FORBIDDEN

    """
    queryset = get_all_courses_certificate_count()
    serializer_class = CourseCertificateSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (BasicAuthentication, SessionAuthentication, OAuth2Authentication)
    throttle_classes = (UserThrottle,)


class CourseCertificateDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get count of certificate for a specific course.

        **Example Requests**

              GET /api/courses/v2/certificates/count/{course_organization}+{course_name}+{course_run}

        **Response Values**

            On success with Response Code <200>

            * course_id: The unique identifier for the course.

            * name: The course name

            * organization: The organization specified for the course.

            * run: The run of the course.

            * certificate_count: Count of certificates for the course

         **ERROR RESPONSES**

                * Response Code <404> COURSE NOT FOUND
                * Response Code <403> FORBIDDEN

    """
    serializer_class = CourseCertificateSerializer
    permission_classes = (IsAdminUser, IsFaculty)
    authentication_classes = (BasicAuthentication, SessionAuthentication, OAuth2Authentication)
    throttle_classes = (UserThrottle,)

    def get_object(self):
        try:
            list = get_certificate_count(self.kwargs['name'], self.kwargs['run'], self.kwargs['org'])
            list['course_id']
            return list
        except:
            raise Http404


class CourseStudentCertificateList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of courses with their students who are getting certificates, in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/courses/v2/certificates/detail/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * course_id: The unique identifier for the course.

                * name: The course name

                * organization: The organization specified for the course.

                * run: The run of the course.

                * students:

                    * id: The unique identifier for the student.

                    * username: Username of the student

                    * email: Email of the student

                    * grade_score: Total score of the student in the course

         **ERROR RESPONSES**

                * Response Code <404> COURSE NOT FOUND
                * Response Code <403> FORBIDDEN

    """
    queryset = get_all_courses_certificate_students()
    serializer_class = CourseStudentCertificateSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (BasicAuthentication, SessionAuthentication, OAuth2Authentication)
    throttle_classes = (UserThrottle,)


class CourseStudentCertificateDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get list of students getting certificate for a specific course.

        **Example Requests**

              GET /api/courses/v2/certificates/detail/{course_organization}+{course_name}+{course_run}

        **Response Values**

            On success with Response Code <200>

            * course_id: The unique identifier for the course.

            * name: The course name

            * organization: The organization specified for the course.

            * run: The run of the course.

            * students:

                * id: The unique identifier for the student.

                * username: Username of the student

                * email: Email of the student

                * grade_score: Total score of the student in the course

         **ERROR RESPONSES**

                * Response Code <404> COURSE NOT FOUND
                * Response Code <403> FORBIDDEN

    """
    serializer_class = CourseStudentCertificateSerializer
    permission_classes = (IsAdminUser, IsFaculty,)
    authentication_classes = (BasicAuthentication, SessionAuthentication, OAuth2Authentication)
    throttle_classes = (UserThrottle,)

    def get_object(self):
        try:
            list = get_certificate_students(self.kwargs['name'], self.kwargs['run'], self.kwargs['org'])
            list['course_id']
            return list
        except:
            raise Http404


class CourseList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of courses in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/courses/v2/courses/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * course_id: The unique identifier for the course.

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

    """
    queryset = get_all_courses_name()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication, OAuth2Authentication)
    throttle_classes = (UserThrottle,)


class CourseGradeList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of courses with all its students in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/courses/v2/detail/

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

                * course_run: The run of the course

                * students:

                    * id: The unique identifier for the student.

                    * username: Username of the student

                    * email: Email of the student

                    * grade: Overall grade of the student in the course

                    * total_score: Total score of the student in the course

                    * is_active: Shows whether the student is active or not
                        1: if student is active
                        0: if student is not active

                    * last_login: The date and time at which the student was last active

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """
    queryset = get_all_courses_details()
    serializer_class = CourseGradeSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    throttle_classes = (UserThrottle,)


class CourseGradeDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get all the students for a specific course.

        **Example Requests**

              GET /api/courses/v2/detail/{course_organization}+{course_name}+{course_run}

        **Response Values**

            On success with Response Code <200>

            * course_name: Name of the course

            * course_organization: The organization specified for the course.

            * course_run: The run of the course

            * students:

                * id: The unique identifier for the student.

                * username: Username of the student

                * email: Email of the student

                * grade: Overall grade of the student in the course

                * total_score: Total score of the student in the course

                * is_active: Shows whether the student is active or not
                    1: if student is active
                    0: if student is not active

                * last_login: The date and time at which the student was last active

         **ERROR RESPONSES**

                * Response Code <404> ORGANIZATION NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = CourseGradeSerializer
    permission_classes = (IsAdminUser, IsFaculty,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    throttle_classes = (UserThrottle,)

    def get_object(self):
        try:
            list = get_all_student_grades(self.kwargs['name'], self.kwargs['run'], self.kwargs['org'])
            list['course_name']
            return list
        except:
            raise Http404