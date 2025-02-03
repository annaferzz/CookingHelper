from django import forms
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instruction', 'image_url']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['recipe', 'name', 'quantity', 'unit']