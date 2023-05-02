from django.db.models import F
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


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

    class Meta:
        model = Recipe
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


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        queryset=Ingredient.objects.all(), slug_field='id'
    )
    # amount = serializers.IntegerField()
    # id = serializers.IntegerField()

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
        # print(validated_data)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        # print(recipe)
        # print('*********', ingredients, '******', sep='\n')
        for ingredient in ingredients:
            print('&&&&&&&&&', ingredient, '&&&&&&&&&', sep='\n')
            # print('&&&&&&&&&', ingredient.get('id'), '&&&&&&&&&', sep='\n')
            # print('&&&&&&&&&', ingredient.get('amount'), '&&&&&&&&&', sep='\n')
            # print('&&&&&&&&&', recipe, '&&&&&&&&&', sep='\n')
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['id'],
            )
        recipe.tags.set(tags)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(
            instance, context=context).data
