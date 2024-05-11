from django.db import models
from courseAdminstration.models import Course
from django.db.models import Count, Case, When, IntegerField, Sum
from django.utils import timezone

# Create your models here.
class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.IntegerField()
    enrollment_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn')
    ], default='enrolled')
    progress_percentage = models.IntegerField(default=0, help_text="Percentage of the course completed, from 0 to 100")

    class Meta:
        unique_together = ('course', 'student')  # Ensure that a student can't be enrolled in the same course twice

    def update_progress(self):
        total_lessons = self.course.get_all_lessons().count()
        completed_lessons = 0

        # Fetch all lessons and manually check for completion
        all_lessons = self.course.get_all_lessons()
        student_id_str = str(self.student)
        for lesson in all_lessons:
            # Split the completed_students string into a list and check membership
            if student_id_str in lesson.completed_students.split(','):
                completed_lessons += 1

        print(f"Total lessons: {total_lessons}, Completed lessons: {completed_lessons}")

        if total_lessons > 0:
            self.progress_percentage = int((completed_lessons / total_lessons) * 100)
        else:
            self.progress_percentage = 0
        
        self.save()
        
    def save(self, *args, **kwargs):
        # Check if the progress is 100% and the status is not already 'completed'
        if self.progress_percentage == 100 and self.status != 'completed':
            self.completion_date = timezone.now()  # Set the completion date to the current date
            self.status = 'completed'  # Update the status to 'completed'

        super().save(*args, **kwargs)
    