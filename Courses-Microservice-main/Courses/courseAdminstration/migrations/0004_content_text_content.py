# Generated by Django 5.0.3 on 2024-04-22 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseAdminstration', '0003_alter_content_lesson_alter_lesson_section_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='text_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
