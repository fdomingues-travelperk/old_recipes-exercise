from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe-list')


def detail_url(recipe_id):
    """Returns the url for a specific recipe"""
    return reverse('recipe-detail', args=[recipe_id])


def create_ingredient(recipe, name='Test ingredient'):
    """Creates a new ingredient for testing"""
    return Ingredient.objects.create(recipe=recipe, name=name)


def create_recipe(ingredients=None, **params):
    """Creates a new recipe for testing"""
    defaults = {
        'name': 'Test Recipe',
        'description': 'Recipe used for testing'
    }
    defaults.update(params)
    recipe = Recipe.objects.create(**defaults)

    if ingredients is None:
        ingredients = ['Ingredient1', 'Ingredient2']

    for ingredient_name in ingredients:
        recipe.ingredients.add(create_ingredient(recipe, ingredient_name))
    return recipe


class RecipeApiTests(TestCase):

    def _verify_ingredients(self, recipe, payload):
        db_ingredients = [ing.name for ing in recipe.ingredients.all()]
        self.assertEqual(len(db_ingredients), len(payload['ingredients']))
        for i in range(len(payload['ingredients'])):
            self.assertIn(payload['ingredients'][i]['name'], db_ingredients)

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieving all the recipes"""
        create_recipe()
        create_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_specific_recipe(self):
        """Test that retrieving it returns a specific single recipe"""
        recipe = create_recipe()
        create_recipe()

        res = self.client.get(detail_url(recipe.id))

        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_with_ingredients(self):
        """Test that a recipe is created with the requested ingredients"""
        payload = {
            'name': 'Hamburger',
            'description': 'A bit of minced meat between two pieces of bread',
            'ingredients': [{'name': 'minced meat'}, {'name': 'bread'}]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self._verify_ingredients(recipe, payload)

    def test_patch_recipe_with_ingredients(self):
        """Test that a recipe is patched and its list of ingredients is updated"""
        recipe = create_recipe(name='Spaghetti',
                               description='Only cooked spaghetti',
                               ingredients=['spaghetti'])

        payload = {
            'description': 'spaghetti with a special sauce',
            'ingredients': [{'name': 'spaghetti'}, {'name': 'carbonara sauce'}]
        }

        res = self.client.patch(detail_url(recipe.id), payload, format='json')

        recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.description, payload['description'])
        self._verify_ingredients(recipe, payload)

    def test_filter_recipes_by_name(self):
        """Test the filtering of recipes by name of the recipe"""
        recipe1 = create_recipe(name='Selected')
        recipe2 = create_recipe(name='Selected v2')
        recipe3 = create_recipe(name='DifferentName')

        res = self.client.get(RECIPES_URL, {'name': 'Select'})

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
