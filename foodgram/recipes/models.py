from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет', max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)


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
    # image = models.ImageField(
    #     upload_to='recipes/images/',
    #     )
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.IntegerField('Время приготовления')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipe')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Ингредиент')
    amount = models.IntegerField('Количество')

    def __str__(self):
        return f'{self.recipe}{self.ingredient}'


class Favourite(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Пользователь',
        related_name='favourite',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, verbose_name='рецепт',
        related_name='favourite',
        on_delete=models.CASCADE
    )


class Subscription(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Пользователь',
        related_name='favourites',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, verbose_name='рецепты',
        related_name='favourites',
        on_delete=models.CASCADE
    )


class ShopingCart(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Пользователь',
        related_name='shoping_cart',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, verbose_name='Корзина',
        related_name='shoping_cart',
        on_delete=models.CASCADE
    )
