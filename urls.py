"""
Course API URI specification.
Patterns here should simply point to version-specific patterns.
"""
from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    '',

    url(r'^v2/', include('course_dashboard_api.v2.urls')),
)
