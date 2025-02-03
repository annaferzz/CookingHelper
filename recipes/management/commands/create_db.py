import csv
import re
from django.core.management.base import BaseCommand
import ast
from recipes.models import Recipe, Ingredient  

def digits(s):
    return any(char.isdigit() for char in s)

class Command(BaseCommand):
    help = 'Import recipes from a CSV file'

    def handle(self, *args, **kwargs):
        with open('./recipes.csv', newline='', encoding='utf-8') as csvfile:  
            reader = csv.DictReader(csvfile)
            for row in reader:
                # создаем рецепт
                recipe = Recipe(
                    name=row['Name'],
                    description=row['Description'],
                    instruction=row['Instruction'],
                    image_url=row['Image URL']
                )
                recipe.save()  

                # Обработка ингредиентов
                ingredients = row['Ingredients'].split(';') 
                for ingredient in ingredients:
                    ingredient = ingredient.split(':')
                    
                    name = ingredient[0].strip()
                    quant_unit = ingredient[1].strip().split() 
                    quantity = ''
                    unit = ''
    
                    for q_u in quant_unit:
                        if digits(q_u):
                            quantity += q_u + ' '
                        else:
                            unit += q_u + ' '

                    quantity = quantity.strip()
                    unit = unit.strip()
                    
                    ingredient = Ingredient(
                        name = name, 
                        recipe_id = recipe, 
                        quantity = quantity,
                        unit = unit
                    )
                    ingredient.save()