from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Ingredient


class CreateRecipes(TestCase):

    def setUp(self):
        self.valid_data = {
            'name': 'Тестовый Рецепт',
            'description': 'Это тестовый рецепт',
            'instruction': 'Сделайте то и то',
            'image_url': 'https://cats.png',
            'form-TOTAL_FORMS': '1',  
            'form-INITIAL_FORMS': '0', 
            'form-MIN_NUM_FORMS': '0', 
            'form-MAX_NUM_FORMS': '1000', 
            'form-0-name': 'Тестовый Ингредиент',  
            'form-0-quantity': '1',  
            'form-0-unit': 'стакан',  
            'form-0-id': '',  
        }

    def test_create_recipe_valid_data(self):
        response = self.client.post(reverse('create_recipes'), data=self.valid_data)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Recipe.objects.count(), 1) 
        self.assertEqual(Ingredient.objects.count(), 1)

    
    def test_create_recipe_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = ''  

        response = self.client.post(reverse('create_recipes'), data=invalid_data)

        self.assertEqual(response.status_code, 200)  
        self.assertEqual(Recipe.objects.count(), 0) 
        self.assertEqual(Ingredient.objects.count(), 0)