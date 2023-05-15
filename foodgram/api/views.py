from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .paginations import LimitPaginations
from .serializers import (AddRecipeSerializer, IngredientSerializer,
                          RecipeFavoriteSerializer, RecipeSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    ordering_fields = ('-pub_date', )
    pagination_class = LimitPaginations

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return AddRecipeSerializer
        return RecipeSerializer

    def add_favorite_or_cart(self, model, user, recipe_id):
        if model.objects.filter(user=user, recipe__id=recipe_id).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeFavoriteSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_favorite_or_cart(self, model, user, recipe_id):
        recipe = model.objects.filter(user=user, recipe__id=recipe_id)
        if recipe.exists():
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        user = request.user
        if request.method == 'POST':
            return self.add_favorite_or_cart(Favorite, user, pk)
        return self.delete_favorite_or_cart(Favorite, user, pk)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = request.user
        if request.method == 'POST':
            return self.add_favorite_or_cart(ShoppingCart, user, pk)
        return self.delete_favorite_or_cart(ShoppingCart, user, pk)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = 'Список покупок'
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        filename = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
