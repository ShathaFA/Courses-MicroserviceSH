from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from courseAdminstration.models import Lesson
from .models import Enrollment, Course
from .serializers import EnrollmentSerializer
from courseAdminstration.serializers import CourseSerializer
from django.conf import settings
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Enrollment

from django.utils import timezone
from rest_framework.views import APIView


@api_view(['POST'])
def enroll_student(request):
    student_id = request.data.get('student')
    course_id = request.data.get('course')
    
    try:
        course = Course.objects.get(id=course_id)
        # Assume student ID is valid or verify with an API call to the "users" microservice
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=student_id,  # Store the student ID directly
            course=course,
            defaults={
                'enrollment_date': timezone.now().date(),
                'status': 'enrolled',
                'progress_percentage': 0
            }
        )
        if created:
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Student already enrolled'}, status=status.HTTP_409_CONFLICT)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UnenrollView(APIView):
    def post(self, request, student, course_id):
        try:
            enrollment = Enrollment.objects.get(student=student, course_id=course_id)
            enrollment.delete()
            return Response({'message': 'Unenrolled successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Enrollment not found'}, status=status.HTTP_404_NOT_FOUND)


#To view all the courses enrolled by a std
class StudentCoursesView(APIView):
    def get(self, request, student):
        print("Student ID:", student)

        enrollments = Enrollment.objects.filter(student=student)
        courses = [enrollment.course for enrollment in enrollments]
        # Pass the student_id to the serializer's context
        print("Courses:", courses)

        serializer = CourseSerializer(courses, many=True, context={'student': student})
        return Response(serializer.data)
    
class EducatorEnrollmentCountView(APIView):
    def get(self, request, instructor):
        # Assuming `educator` is a field in the `Course` model linking to the educator
        courses = Course.objects.filter(instructor=instructor)
        total_enrolled_students = Enrollment.objects.filter(course__in=courses).count()
        return Response({"total_enrolled_students": total_enrolled_students})    
    
class CompleteLessonView(APIView):
    def post(self, request, lesson_id):
        user_id = request.data.get('userId')
        if not user_id:
            return Response({'success': False, 'message': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            if lesson.mark_as_completed(user_id):
                lesson.update_enrollment_progress(user_id)
                print("updated enrollement was called")
                return Response({'success': True, 'message': 'Lesson marked as completed'})
            else:
                return Response({'success': False, 'message': 'User already completed this lesson'}, status=status.HTTP_409_CONFLICT)
        except Lesson.DoesNotExist:
            return Response({'success': False, 'message': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)




@require_http_methods(["GET"])
def get_completed_courses_count(request, student):
    count = Enrollment.objects.filter(student=student, status='completed').count()
    return JsonResponse({'completed_courses_count': count})


def get_course_counts(request, student):
    completed_courses = Enrollment.objects.filter(student=student, status='completed').count()
    total_enrolled_courses = Enrollment.objects.filter(student=student).count()
    
    return JsonResponse({
        'completed_courses': completed_courses,
        'total_enrolled_courses': total_enrolled_courses
    })