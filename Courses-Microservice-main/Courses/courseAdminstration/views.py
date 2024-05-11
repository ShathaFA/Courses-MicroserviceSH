from rest_framework import generics, permissions, status

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Course, Course, Section, Lesson, Content
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework.decorators import api_view
from .serializers import CourseSerializer, SectionSerializer, LessonSerializer, ContentSerializer
from rest_framework.generics import CreateAPIView
import requests



def get_instructor_name_by_id(instructor_id):
    response = requests.get(f"http://users_microservice_url/api/instructors/{instructor_id}")
    if response.status_code == 200:
        return response.json()['name']
    else:
        return "Unknown Instructor"  # Fallback if the request fails or no name is found

class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

def listAllCourses(request):
    # No context is passed here because data will be loaded via AJAX
    return render(request, 'courses.html')


# For creating a new course
# class CourseCreateView(generics.CreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

class CourseCreateView(APIView):
    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # This will help in debugging during development
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
def createCourse(request):
    # No context is passed here because data will be loaded via AJAX
    return render(request, 'firstPageOfCreateCourse.html')

class CourseUpdate(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDelete(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


def courseinfo(request):
    course_id = request.GET.get('courseId')
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courseinfo.html', {'course': course})


class CourseDetailView(APIView):
    def get(self, request, pk):
        # Use prefetch_related to ensure related sections (and nested relations if needed) are fetched
        course = get_object_or_404(Course.objects.prefetch_related('sections'), pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    
    
def CourseInner(request):
    return render(request,'CourseInner.html')


@api_view(['POST'])
def create_section(request):
    serializer = SectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_BAD_REQUEST)

@api_view(['POST'])
def create_lesson(request):
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# To get a course element for a certain edu
class EduCourseListView(APIView):
    """
    List all courses for a given educator.
    """
    def get(self, request, format=None):
        instructor = request.query_params.get('instructor')
        if instructor is not None:
            courses = get_list_or_404(Course, instructor=instructor)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Educator ID must be provided."}, status=400)
        
        
class PublishedCoursesView(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', None)
        print("Received search query:", search_query)  # Debugging output
        published_courses = Course.objects.filter(isPublished=True)
        if search_query:
            published_courses = published_courses.filter(title__icontains=search_query)
            print("Filtered courses count:", published_courses.count())  # Debugging output
        serializer = CourseSerializer(published_courses, many=True)
        return Response(serializer.data)

    

class SectionCreateView(APIView):
    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)  # Ensure your Section model has a foreign key to Course
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LessonCreateView(APIView):
    def post(self, request, section_id):
        try:
            section = Section.objects.get(pk=section_id)
            serializer = LessonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(section=section)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
@api_view(['DELETE'])
def delete_section(request, section_id):
    try:
        section = Section.objects.get(pk=section_id)
        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Section.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['DELETE'])
def delete_lesson(request, lesson_id):
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'pk'  # This tells DRF to find the Lesson by its primary key

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
class SectionUpdateView(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    lookup_field = 'pk'  # Use primary key to identify the section

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    

class ContentCreateUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        content = get_object_or_404(Content, pk=request.data.get('id'))  # Safely retrieve content or return 404
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CourseDeleteView(generics.DestroyAPIView):
    # TODO: Re-enable authentication and permissions before moving to production
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        self.perform_destroy(course)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class TogglePublishCourseView(APIView):
    def patch(self, request, pk):
        course = Course.objects.get(pk=pk)
        course.isPublished = not course.isPublished
        course.save()
        return Response({"id": course.id, "isPublished": course.isPublished}, status=status.HTTP_200_OK)
    
    
    
