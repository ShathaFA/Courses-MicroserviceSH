from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('<int:pk>/', views.CourseDetail.as_view(), name='course-detail'),
    path('<int:pk>/update/', views.CourseUpdate.as_view(), name='course-update'),
    path('<int:pk>/delete/', views.CourseDelete.as_view(), name='course-delete'),


    path('listAllCourses/api/', views.CourseList.as_view(), name='CourseList'),
    path('listAllCourses/', listAllCourses, name='listAllCourses'),

    path('createCourse/api/', views.CourseCreateView.as_view(), name='CourseCreateView'),
    path('createCourse/', createCourse, name='createCourse'),

    path('courseinfo/',views.courseinfo, name = 'courseinfo'),
    path('courses/api/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('sections/api/', views.create_section, name='create-section'),
    path('lessons/api/', views.create_lesson, name='create-lesson'),

    path('CourseInner',views.CourseInner, name = 'CourseInner'),

    path('eduCourses/api/', EduCourseListView.as_view(), name='edu-courses-list'),
    path('publishedCourses/api/', PublishedCoursesView.as_view(), name='published-courses'),


    path('<int:course_id>/sections/', SectionCreateView.as_view(), name='section-create'),
    path('sections/<int:section_id>/lessons/', LessonCreateView.as_view(), name='lesson-create'),
    path('deleteSections/<int:section_id>/', delete_section, name='delete_section'),
    path('deleteLessons/<int:lesson_id>/', delete_lesson, name='delete_lesson'),


    path('updateLesson/api/<int:pk>/', LessonUpdateView.as_view(), name='update-lesson'),
    path('updateSection/api/<int:pk>/', SectionUpdateView.as_view(), name='update-section'),
    path('content/', ContentCreateUpdateView.as_view(), name='content-create-update'),
    path('content/<int:id>/', ContentCreateUpdateView.as_view(), name='content-update'),  # For PUT



    path('delete/<int:pk>/', CourseDeleteView.as_view(), name='course-delete'),
    path('togglePublish/<int:pk>/', TogglePublishCourseView.as_view(), name='toggle-publish'),
    

]

