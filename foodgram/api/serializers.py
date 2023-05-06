from django.db.models import F
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, Favorite, ShoppingCart


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class AddTagToRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id')


class RecipeSerializer(serializers.ModelSerializer):
    """Получение рептов."""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        # fields = (
        #     'id', 'tags', 'author',
        #     'ingredients', 'is_favorited',
        #     'is_in_shopping_cart', 'name',
        #     'image', 'text', 'cooking_time'
        # )
        fields = '__all__'

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe_ingredient__amount')
        )
        return ingredients

    def get_is_favorite(self, recipe):
        user = self.context.get('request').user
        return (
            user.is_authenticated and
            Favorite.objects.filter(user=user, recipe=recipe).exists()
        )

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        return (
            user.is_authenticated and
            ShoppingCart.objects.filter(user=user, recipe=recipe).exists()
        )


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['id'],
            )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
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

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')
