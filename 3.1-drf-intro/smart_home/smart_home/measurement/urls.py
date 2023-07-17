from django.urls import path

from measurement.views import CreateSensor, UpdateSensor, AddMeasurement, \
    list_sensors, sensors_details

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('list/', list_sensors),
    path('details/<int:id>', sensors_details),
    path('create', CreateSensor.as_view()),
    path('add/', AddMeasurement.as_view()),
    path('update/<pk>', UpdateSensor.as_view()),
]
