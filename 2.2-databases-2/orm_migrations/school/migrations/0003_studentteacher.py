# Generated by Django 4.2.1 on 2023-05-06 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0002_remove_student_teacher_student_teachers_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentTeacher",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="school.student"
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="school.teacher"
                    ),
                ),
            ],
        ),
    ]
