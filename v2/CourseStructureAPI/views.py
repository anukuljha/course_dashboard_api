from rest_framework import generics
from api import *
from serializers import CourseStructureSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication

# Create your views here.


class CourseStructureList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of courses with their structures in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/courses/v2/structures/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * course_id: The unique identifier for the course.
                
                * section: Each sections of the course
                    
                    * name: Name of the section
                    
                    * subsection: Each subsections of the section
                    
                        * name: Name of the subsection
                        
                        * unit: Each units of the subsection
                    
                            * name: Name of the unit

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """
    queryset = get_all_courses_structure()
    serializer_class = CourseStructureSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class CourseStructureDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get course structure for a specific course.

        **Example Requests**

              GET /api/courses/v2/structures/{course_organization}+{course_name}+{course_run}

        **Response Values**

            On success with Response Code <200>

            * course_id: The unique identifier for the course.
                
                * section: Each sections of the course
                    
                    * name: Name of the section
                    
                    * subsection: Each subsections of the section
                    
                        * name: Name of the subsection
                        
                        * unit: Each units of the subsection
                    
                            * name: Name of the unit

         **ERROR RESPONSES**

                * Response Code <404> COURSE NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = CourseStructureSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            list = get_course_structure(self.kwargs['name'], self.kwargs['run'], self.kwargs['org'])
            list['course_id']
            return list
        except:
            raise Http404