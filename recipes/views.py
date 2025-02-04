from django.shortcuts import render, redirect
from .forms import RecipeForm, IngredientFormSet
from .models import Ingredient
from django.contrib import messages
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
