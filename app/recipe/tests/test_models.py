from django.test import TestCase

from recipe import models


class ModelTests(TestCase):

    def test_recipe_str(self):
        """Test that the string representation of recipe is correct"""
        recipe = models.Recipe.objects.create(
            name='Test Recipe',
            description='A recipe used for tests'
        )

        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test that the string representation of ingredient is correct"""
        recipe = models.Recipe.objects.create(name='Banana Smoothie', description='The name says it all, really')
        ingredient = models.Ingredient.objects.create(
            name='Bananas',
            recipe=recipe
        )

        self.assertEqual(str(ingredient), ingredient.name)
