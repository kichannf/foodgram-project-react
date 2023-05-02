from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class AddTagToRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', )


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    # def create(self, validated_data):
    #     tags = validated_data.pop('tags')
    #     recipe = Recipe.objects.create(**validated_data)
    #     for tag in tags:
    #         Tag.objects.create(recipe=recipe, **tags)
    #     return recipe
