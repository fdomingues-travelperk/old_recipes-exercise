from django.db import models


class Recipe(models.Model):
    """Represents a recipe"""

    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Represents the ingredients to be used on a Recipe"""

    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
