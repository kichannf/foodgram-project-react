from rest_framework import viewsets
from rest_framework.decorators import action

from recipes.models import Favorite,Ingredient, Recipe, Tag
from .serializers import (
    AddRecipeSerializer,
    IngredientSerializer, RecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return AddRecipeSerializer
        return RecipeSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, id):
        ...
