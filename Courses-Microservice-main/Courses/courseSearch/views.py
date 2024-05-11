from django.http import JsonResponse
from django.views import View
from courseAdminstration.models import Course
from django.db.models import Q

class SearchCourses(View):
    def get(self, request):
        query = request.get('query', '')
        category = request.get('category', 'All')

        # Filter courses based on query and category
        if category != 'All':
            courses = Course.objects.filter(Q(title__icontains=query) | Q(category__icontains=category))
        else:
            courses = Course.objects.filter(title__icontains=query)

        # Serialize the courses data
        data = [{'id': course.id, 'title': course.title, 'coursePic': course.coursePic} for course in courses]
        return JsonResponse(data, safe=False)