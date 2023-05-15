from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет', max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        related_name='recipe',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipe'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        verbose_name='Картинка'
    )
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Время приготовление должно быть больше 0'),),
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата')

    class Meta:
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                1, message='Количество ингредиентов должно быть больше 0'),),
    )

    class Meta:
        ordering = ('ingredient__name', )

    def __str__(self):
        return f'{self.recipe}{self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь',
        related_name='favorite',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, verbose_name='рецепт',
        related_name='favorite',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('user', )
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            ),
        )

    def __str__(self):
        return f'{self.recipe} у {self.user} в избранном'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь',
        related_name='shopping_cart',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, verbose_name='Корзина',
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('user', )

    def __str__(self):
        return f'{self.recipe} у {self.user} в списке покупок'
