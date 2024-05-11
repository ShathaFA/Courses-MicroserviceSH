import json
from django.db import models
from django.db.models import JSONField

class Course(models.Model):
    title = models.CharField(max_length=100)
    instructor= models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    difficultyLevel = models.CharField(max_length=100)
    coursePic = models.ImageField(upload_to='course_pics/',default='course_pics/defaultCourse.jpg', blank=True, null=True)
    
    isPublished = models.BooleanField(default=False)
    average_rating = models.FloatField(default=0.0, blank=True)

 
    def get_all_lessons(self):
        # This will collect all lessons from all sections of the course
        return Lesson.objects.filter(section__course=self)
    
    def __str__(self):
        return self.title
    
    def update_average_rating(self):
        ratings = self.ratings.all()  # Assuming a reverse relation from Rating to Course
        if ratings:
            total_rating = sum(rating.stars for rating in ratings)
            self.average_rating = total_rating / len(ratings)
            self.save()
 
class Section(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    
    def __str__(self):
        return self.title 

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    section = models.ForeignKey('Section', on_delete=models.CASCADE,related_name='lessons' )
    completed_students = models.TextField(default="")  # Will store user IDs as "id1,id2,id3"

    def mark_as_completed(self, user_id):
        if user_id not in self.completed_students.split(','):
            if self.completed_students:
                self.completed_students += f',{user_id}'
            else:
                self.completed_students = str(user_id)
            self.save()
            return True
        return False

    def __str__(self):
        return self.title

    def update_enrollment_progress(self, user_id):
        from courseEnrollement.models import Enrollment  # Import here to avoid circular dependency
        print("updated enrollement was accessed")

        try:
            enrollment = Enrollment.objects.get(course=self.section.course, student=user_id)
            enrollment.update_progress()
        except Enrollment.DoesNotExist:
            # Handle the case where enrollment does not exist if necessary
            pass
 
class Content(models.Model):
    LESSON_CONTENT_CHOICES = (
        ('vid', 'Video'),
        ('img', 'Image'),
        ('txt', 'Text'),
        ('voc', 'Voice'),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='contents')
    type = models.CharField(max_length=3, choices=LESSON_CONTENT_CHOICES)
    reference = models.CharField(max_length=255, null=True, blank=True)  # Keep for non-text content
    text_content = models.TextField(null=True, blank=True)  # Additional field for text content

    def __str__(self):
        return f"{self.lesson.title} - {self.type}"
     
class Quiz(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True, blank=True)
    mark = models.DecimalField(max_digits=5, decimal_places=2, default=0)
   

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
   
    def choices(self):
        return [self.choice1, self.choice2, self.choice3, self.choice4]
 
 
 
 
class SelectedChoice(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
 
    class Meta:
        # Define composite primary key with student and quiz
        constraints = [
            models.UniqueConstraint(fields=['student', 'quiz'], name='unique_selected_choice')
        ]
 
class QuestionGrade(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # Other fields related to grading, like grade, etc.
 
    class Meta:
        # Define composite primary key with student and quiz
        constraints = [
            models.UniqueConstraint(fields=['student', 'quiz'], name='unique_question_grade')
        ]
 
    def calculate_received_mark(self):
        total_questions = self.quiz.question_set.count()
        total_correct = 0
 
        # Iterate over questions in the quiz
        for question in self.quiz.question_set.all():
            # Check if the user's answer matches the correct answer
            # For simplicity, assuming correct answers are stored in the database
            if self.selectedchoice_set.filter(question=question, selected_answer=question.correct_answer).exists():
                total_correct += 1
 
        # Calculate the received mark based on the number of correct answers
        received_mark = (total_correct / total_questions) * 100
        return received_mark
    
    
class Rating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    user = models.IntegerField()
    stars = models.IntegerField()

    class Meta:
        unique_together = [['user', 'course']]  # Each user can only rate a course once