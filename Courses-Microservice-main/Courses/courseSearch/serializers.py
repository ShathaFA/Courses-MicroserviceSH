from rest_framework import serializers
from courseAdminstration.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'  # Serialize all fields in the Course model