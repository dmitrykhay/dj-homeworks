from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        if not self.instance or data.get('status') == 'OPEN':
            user = self.context["request"].user
            if Advertisement.objects.filter(creator=user, status="OPEN").count() >= 10:
                raise serializers.ValidationError(
                    "Пользователь не может иметь больше 10 открытых объявлений!"
                )

        return data


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    favorite = AdvertisementSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'favorite',)

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        if data['advertisement'].creator == data['user']:
            raise serializers.ValidationError("Это ваше объявление!")
        elif Favorite.objects.filter(
                user=data['user'],
                advertisement=data['advertisement']
        ):
            raise serializers.ValidationError("И так в избранном!")
        return data
