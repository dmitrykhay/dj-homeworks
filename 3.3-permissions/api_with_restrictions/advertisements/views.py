from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import MyReadOnly
from advertisements.serializers import AdvertisementSerializer, \
    FavoriteAdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return Advertisement.objects.all()
        elif self.request.user.is_anonymous:
            return Advertisement.objects.exclude(status='DRAFT')
        elif self.request.user.is_authenticated:
            return Advertisement.objects.filter(creator=self.request.user) | Advertisement.objects.exclude(status='DRAFT')

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['create', "add_to_favorite"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), MyReadOnly()]
        return []

    @action(methods=['post'], detail=True)
    def add_to_favorite(self, request, pk=None):
        queryset = Advertisement.objects.filter(id=pk).first()
        if queryset:
            validated_data = {'advertisement': queryset, 'user': request.user}
            serializer = FavoriteAdvertisementSerializer()
            serializer.validate(validated_data)
            serializer.create(validated_data)
            return Response('Объявление добавлено в избранное', status=status.HTTP_201_CREATED)
        return Response('Такого объявления нет', status=status.HTTP_204_NO_CONTENT)
