# Generated by Django 5.0.3 on 2024-05-10 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseAdminstration', '0009_alter_lesson_completed_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='average_rating',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('stars', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='courseAdminstration.course')),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
    ]
