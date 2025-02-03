from django.shortcuts import render, redirect
from .models import Recipe, Ingredient

def send_recipes(request):
    recipes = Recipe.objects.order_by('name')
    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/send_recipes.html', {'recipes':recipes, 'ingredients':ingredients})
