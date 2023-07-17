from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django_testing import settings
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        if data.get("students"):
            if len(data["students"]) > settings.MAX_STUDENTS_PER_COURSE:
                raise ValidationError(
                    f"Can't add more than {settings.MAX_STUDENTS_PER_COURSE}"
                )
        return data
