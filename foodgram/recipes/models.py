from django.db import models

# Create your models here.
class Tags(models.Model):
    name = models.CharField('Название', max_length=200, unique=True, blank=True, null=True)
    tags = models.CharField('Цвет', max_length=7, unique=True, blank=True, null=True)
    slug = slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)


class Recipe(models.Model):
    ...