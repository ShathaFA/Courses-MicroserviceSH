from django.contrib import admin
from .models import Course, Section, Lesson, Content ,Quiz ,Question

# Register your models here.
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lesson)
admin.site.register(Content)
admin.site.register(Quiz)
admin.site.register(Question)
