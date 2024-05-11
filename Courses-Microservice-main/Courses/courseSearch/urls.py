from django.urls import path
from .views import SearchCourses

urlpatterns = [
    path('search-courses/', SearchCourses.as_view(), name='search_courses'),
    # Other URL patterns as needed
]
