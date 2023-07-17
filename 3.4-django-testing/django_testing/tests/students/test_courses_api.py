import pytest
from rest_framework.test import APIClient
from model_bakery import baker
import json

from django_testing import settings
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/{courses[0].id}/')
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == courses[0].id


@pytest.mark.django_db
def test_get_list_course(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == 200
    for i, course in enumerate(data):
        assert course['id'] == courses[i].id


@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    courses = course_factory(_quantity=10)
    for i, course in enumerate(courses):
        response = client.get('/api/v1/courses/', data={'id': course.id})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['id'] == courses[i].id


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    courses = course_factory(_quantity=10)
    for i, course in enumerate(courses):
        response = client.get('/api/v1/courses/', data={'name': course.name})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['name'] == courses[i].name


@pytest.mark.django_db
def test_create_course(client):
    courses = Course.objects.create(name='Python')
    response = client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == courses.name


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.patch(
        f'/api/v1/courses/{courses[0].id}/',
        data={'name': 'Python'}
    )

    assert response.status_code == 200
    assert response.json()['name'] != courses[0].name


@pytest.mark.django_db
def test_max_students_ok(client, course_factory):
    settings.MAX_STUDENTS_PER_COURSE = 1
    courses = course_factory(_quantity=1)
    student = Student.objects.create(name="Evgeny")
    response = client.patch(
        f'/api/v1/courses/{courses[0].id}/',
        data={'students': [student.id]}
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_max_students_error(client, course_factory):
    settings.MAX_STUDENTS_PER_COURSE = 0
    courses = course_factory(_quantity=1)
    student = Student.objects.create(name="Evgeny")
    response = client.patch(
        f'/api/v1/courses/{courses[0].id}/',
        data={'students': [student.id]}
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')

    assert response.status_code == 204
