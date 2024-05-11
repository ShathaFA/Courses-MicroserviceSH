# serializers.py

from rest_framework import serializers
from courseAdminstration.models import Course, Section, Lesson, Content, Quiz, Question, SelectedChoice, QuestionGrade

from rest_framework import serializers

class GenerateCourseContentSerializer(serializers.Serializer):
    title = serializers.CharField()
    category = serializers.CharField()
    difficultyLevel = serializers.CharField()
    # Define other fields as needed

class GenerateMCQsSerializer(serializers.Serializer):
    topic = serializers.CharField()
    number_of_questions = serializers.IntegerField(min_value=1)  # Example validation

    # Add any other fields or validations as needed

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'  # Include all fields in serialization

    # Ensure that 'id' field is explicitly handled for serialization
    id = serializers.IntegerField()
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class GenerateLessonContentSerializer(serializers.Serializer):
    course_name = serializers.CharField()
    course_description = serializers.CharField()
    section_name = serializers.CharField()
    section_description = serializers.CharField()
    lesson_name = serializers.CharField()