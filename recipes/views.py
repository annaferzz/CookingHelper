from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Ingredient
from django.core.paginator import Paginator
import nltk
from .forms import RecipeForm, IngredientFormSet
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView

def create_recipes(request):
    print(request.POST)
    recipe_form = RecipeForm(request.POST)
    ingredient_formset = IngredientFormSet(request.POST)

    if recipe_form.is_valid() and ingredient_formset.is_valid():
        recipe = recipe_form.save()

        for form in ingredient_formset:
            if form.cleaned_data:  
                ingredient = form.save(commit=False)
                ingredient.recipe_id = recipe
                ingredient.save()

        return redirect('recipes')
    else:
        recipe_form = RecipeForm()
        ingredient_formset = IngredientFormSet(queryset=Ingredient.objects.none())

    return render(request, 'recipes/create_recipes.html', {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset})

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
