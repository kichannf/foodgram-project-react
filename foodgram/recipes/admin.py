from django.contrib import admin
from django.contrib.admin import display
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class IngredientInRecipe(admin.TabularInline):
    model = Ingredient


class TagInRecipe(admin.TabularInline):
    model = Tag


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('name', 'author', 'count_favorite')
    list_filter = ('name', 'author', 'tags')
    inlines = [IngredientInRecipe, TagInRecipe]

    @display(description='Кол-во в избранном')
    def count_favorite(self, recipe):
        return recipe.favorite.count()


class IngredientResourse(resources.ModelResource):

    class Meta:
        model = Ingredient
        fields = (
            'name', 'measurement_unit'
        )
        import_id_fields = (
            'name', 'measurement_unit'
        )


class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResourse
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', )


class TagResourse(resources.ModelResource):

    class Meta:
        model = Tag
        fields = (
            'name', 'color', 'slug'
        )
        import_id_fields = (
            'name', 'color', 'slug'
        )


class TagAdmin(ImportExportModelAdmin):
    resource_class = TagResourse
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
