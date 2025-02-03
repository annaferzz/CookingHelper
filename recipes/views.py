from django.shortcuts import render, get_object_or_404
from .models import Recipe, Ingredient
from django.core.paginator import Paginator
import nltk


def send_recipes(request):
    recipes = Recipe.objects.order_by('name')
    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/send_recipes.html', {'recipes': recipes, 'ingredients': ingredients})


def page_recipes(request):
    recipes_list = Recipe.objects.order_by('name')
    paginator = Paginator(recipes_list, 12)
    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)
    return render(request, 'recipes/page_recipes.html', {'recipes': recipes})


def detail_recipes(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    steps = nltk.sent_tokenize(recipe.instruction, language='russian')
    ingredients = Ingredient.objects.filter(recipe_id=recipe_id)
    return render(request, 'recipes/detail_recipes.html', {'recipe': recipe,
                                                           'ingredients': ingredients, 'steps': steps}, )
