from django_filters import rest_framework as filters
from django_filters.rest_framework import DateFromToRangeFilter

from advertisements.models import Advertisement, Favorite


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = DateFromToRangeFilter()
    favorites = filters.CharFilter(method='filter_by_favorites')

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at', 'favorites', 'status']

    def filter_by_favorites(self, queryset):
        """
        Фильтрует объявления по избранным объявлениям пользователя.
        """
        favorites = Favorite.objects.filter(user=self.request.user)
        favorite_advertisements_ids = [fav.advertisement.id for fav in
                                       favorites]
        return queryset.filter(id__in=favorite_advertisements_ids)
