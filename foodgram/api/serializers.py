import base64

from django.core.files.base import ContentFile
from django.db.models import F

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.serializers import MyUserSerializer


class Base64ImageField(serializers.ImageField):
    """Сериализатор для поля картинки."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Получение рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True, allow_null=True)
    author = MyUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe_ingredient__amount')
        )
        return ingredients

    def get_is_favorited(self, recipe):
        request = self.context.get('request')
        return (
            request.user.is_authenticated and
            Favorite.objects.filter(user=request.user, recipe=recipe).exists()
        )

    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get('request')
        return (
            request.user.is_authenticated and
            ShoppingCart.objects.filter(user=request.user, recipe=recipe
                                        ).exists()
        )


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    """Добавление ингредиентов в рецепт."""

    id = serializers.SlugRelatedField(
        queryset=Ingredient.objects.all(), slug_field='id'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class AddRecipeSerializer(serializers.ModelSerializer):
    """Добавление рецептов."""

    tags = serializers.SlugRelatedField(
        many=True, queryset=Tag.objects.all(), slug_field='id')
    ingredients = AddIngredientToRecipeSerializer(many=True)
    image = Base64ImageField(allow_null=True)
    author = MyUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time', 'author'
        )

    def create(self, validated_data):
        author = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data, author=author)
        for ingredient in ingredients:
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['id'],
            )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        author = self.context['request'].user
        if instance.author != author:
            raise ValidationError('Изменить рецепт может только автор!')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        recipe = super().update(instance, validated_data)
        recipe.tags.clear()
        recipe.ingredients.clear()
        recipe.tags.set(tags)
        for ingredient in ingredients:
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['id'],
            )
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(
            instance, context=context).data


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """Добавление в избранное."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
