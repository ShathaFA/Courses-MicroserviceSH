# Generated by Django 5.0.3 on 2024-03-16 01:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('instructor', models.IntegerField()),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('duration', models.DurationField()),
                ('difficultyLevel', models.CharField(max_length=20)),
                ('coursePic', models.ImageField(blank=True, null=True, upload_to='course_pics/')),
                ('isPublished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('lessonID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('text', 'Text'), ('video', 'Video'), ('audio', 'Audio'), ('picture', 'Picture')], max_length=20)),
                ('content', models.TextField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseAdminstration.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('sectionID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseAdminstration.course')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseAdminstration.section'),
        ),
    ]