from django.conf import settings
from rest_framework import serializers
from .models import Course, Section, Lesson, Content
from courseEnrollement.models import Enrollment

class ContentSerializer(serializers.ModelSerializer):
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), source='lesson', write_only=True)

    class Meta:
        model = Content
        fields = ['id', 'lesson_id', 'type', 'reference', 'text_content']

    def to_representation(self, instance):
        """Dynamically adjust fields based on the content type."""
        ret = super().to_representation(instance)
        if instance.type == 'txt':
            ret.pop('reference', None)  # Remove reference field for text content
        elif instance.type in ['vid', 'img', 'voc']:
            ret.pop('text_content', None)  # Remove text_content for non-text types
        return ret

    def validate(self, data):
        """Custom validation to check content type-specific requirements."""
        if data['type'] == 'txt' and not data.get('text_content'):
            raise serializers.ValidationError("Text content is required for text type.")
        if data['type'] in ['vid', 'img', 'voc'] and not data.get('reference'):
            raise serializers.ValidationError("Reference is required for video, image, and voice types.")
        return data

class LessonSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)  # Corrected source

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'contents', 'completed_students']  # Include 'completed_students'

class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # Corrected source

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'lessons']

class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    coursePic = serializers.ImageField(use_url=True, required=False, allow_null=True)
    enrolled_students = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'instructor', 'category', 'description', 'duration', 'difficultyLevel', 'coursePic', 'isPublished','progress_percentage', 'enrolled_students', 'sections']
        extra_kwargs = {
            'coursePic': {'required': False}
        }

    def get_enrolled_students(self, obj):
        # Calculate the number of students enrolled in each course
        return Enrollment.objects.filter(course=obj).count()


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.coursePic:
            pic_url = instance.coursePic.url if instance.coursePic else None
            if pic_url and not pic_url.startswith(("http:", "https:")):
                pic_url = settings.SITE_DOMAIN + pic_url
            representation['coursePic'] = pic_url
        return representation
    
    
    def get_progress_percentage(self, obj):
        student = self.context.get('student')
        enrollment = Enrollment.objects.filter(course=obj, student=student).first()
        print("Progress percentage for student:", student, "is", enrollment.progress_percentage if enrollment else "No enrollment found")
        return enrollment.progress_percentage if enrollment else 0
    
    