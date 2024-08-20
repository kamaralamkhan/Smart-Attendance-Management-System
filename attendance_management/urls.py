# attendance_management/urls.py

from django.contrib import admin
from django.urls import path
from students.views import student_login, teacher_login, student_list, view_attendance,dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', student_login, name='student_login'),
    path('', teacher_login, name='teacher_login'), #access by root directory in borwser
    # path('teacher/', teacher_login, name='teacher_login'), access by teacher/
    path('student_list/', student_list, name='student_list'),
    path('view_attendance/', view_attendance, name='view_attendance'),  # add the new view
    path('dashboard/', dashboard, name='dashboard'),  # New URL pattern for the dashboard

    # path('', base)
    # Add other URL patterns here as needed
]
