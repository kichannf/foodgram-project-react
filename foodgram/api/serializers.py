from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag


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


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Получение рептов."""
    tags = TagSerializer(many=True, read_only=True)
    # ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    # def get_ingredients():
    #     ...


class AddRecipeSerializer(serializers.ModelSerializer):
    """Добавление рецептов."""
    tags = serializers.SlugRelatedField(
        many=True, queryset=Tag.objects.all(), slug_field='id')
    ingredients = AddIngredientToRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    # def create(self, validated_data):
    #     tags = validated_data.pop('tags')
    #     recipe = Recipe.objects.create(**validated_data)
    #     for tag in tags:
    #         Tag.objects.create(recipe=recipe, **tags)
    #     return recipe
