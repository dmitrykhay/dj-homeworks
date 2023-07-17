# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response

from .models import Sensor
from .serializers import SensorDetailSerializer, SensorSerializer, \
    MeasurementSerializer


class CreateSensor(CreateAPIView):
    serializer_class = SensorSerializer


class UpdateSensor(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class AddMeasurement(CreateAPIView):
    serializer_class = MeasurementSerializer


@api_view(['GET'])
def list_sensors(request):
    sensors = Sensor.objects.all()
    serializer = SensorSerializer(sensors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def sensors_details(request, id):
    sensors = Sensor.objects.get(id=id)
    serializer = SensorDetailSerializer(sensors)
    return Response(serializer.data)
