from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    tags = models.CharField('Цвет', max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    quantity = models.IntegerField('Количество')
    measurement_unit = models.CharField('Единица измерения', max_length=200)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipe')
    name = models.CharField('Название', max_length=200)
    # image = models.ImageField(
    #     upload_to='recipes/images/',
    #     )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        related_name='recipe',
        through='RecipeIngredient'
    )
    tag = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField('Время приготовления')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe}{self.ingredient}'
