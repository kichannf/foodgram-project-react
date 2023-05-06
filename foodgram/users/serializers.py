from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .models import Follow
from api.serializers import RecipeFavoriteSerializer

User = get_user_model()


class MyCreateUserSerializers(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class MyUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if Follow.objects.filter(user=user, following=obj).exists():
            return True
        return False


class SubscribeSerializer(MyUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(MyUserSerializer.Meta):
        fields = MyUserSerializer.Meta.fields + (
            'recipes', 'recipes_count'
        )
        read_only_fields = ('email', 'username')

    def validate(self, data):
        user = self.context.get('request').user
        following = self.instance
        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError(
                'Упс, вы уже подписаны на автора!'
            )
        if user == following:
            raise ValidationError(
                'Упс, нельзя подписаться на себя'
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeFavoriteSerializer(
            recipes, many=True, read_only=True)
        return serializer.data
