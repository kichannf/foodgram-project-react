from rest_framework import mixins, viewsets

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from .serializers import (
    IngredientSerializer, RecipeSerializer, TagSerializer, RecipeIngredient)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = IngredientSerializer
