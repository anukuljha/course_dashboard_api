# course_dashboard_api

## Course Dashboard API version 2

The APIs in this repository, are for Open edX platform.

### Installation

* Clone the repository:

  https://github.com/jaygoswami2303/course_dashboard_api.git
  
* In folder v2, python file dbv.py stores the database details for MySQL and Mongo, update MySQL database username/password as per the open edX server.

* Copy the API folder (course_dashboard_api) to the folder, /edx/app/edxapp/edx-platform/lms/djangoapps/

* Add the name of the app (course_dashboard_api) in the key ‘INSTALLED_APPS’ in python file /edx/app/edxapp/edx-platform/lms/envs/common.py

```python
INSTALLED_APPS = (

...

'course_dashboard_api’ ,

)
```

* Add the urls of the app (course_dashboard_api) to ‘url_patterns’ in python file /edx/app/edxapp/edx-platform/lms/urls.py

```python
urlpatterns = (

...

url(r’^api/courses’, include(‘course_dashboard_api.urls’)),

)
```

* Restart LMS and CMS servers by the command:
```bash
sudo /edx/bin/supervisorctl restart edxapp:
```


### [Documentation for APIs](https://github.com/jaygoswami2303/course_dashboard_api/wiki)

#### NOTE
The GRADE endpoint works for Ficus release.
