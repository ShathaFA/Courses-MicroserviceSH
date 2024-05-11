from rest_framework import serializers
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    enrollment_date = serializers.DateField(input_formats=['%Y-%m-%d', 'iso-8601'])

    class Meta:
        model = Enrollment
        fields = ['course', 'student', 'enrollment_date', 'status', 'progress_percentage']
