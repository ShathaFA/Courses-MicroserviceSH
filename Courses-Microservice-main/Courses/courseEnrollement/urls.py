# courses/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('api/enroll/', enroll_student, name='enroll_student'),
    path('api/student/<int:student>/courses/', StudentCoursesView.as_view(), name='student_courses'),
    path('api/unenroll/<int:student>/<int:course_id>/', UnenrollView.as_view(), name='unenroll'),
    path('enrollment-count/<int:instructor>/', EducatorEnrollmentCountView.as_view(), name='educator-enrollment-count'),

    path('api/lessons/<int:lesson_id>/complete', CompleteLessonView.as_view(), name='complete-lesson'),

    path('api/get_completed_courses_count/<int:student>/', get_completed_courses_count, name='get-completed-courses-count'),
    path('api/get_course_counts/<int:student>/', get_course_counts, name='get-course-counts'),

]
