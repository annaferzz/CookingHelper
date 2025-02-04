from django import forms
from .models import Recipe, Ingredient
from django.forms import modelformset_factory

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instruction', 'image_url']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'instruction': 'Инструкция',
            'image_url': 'Ссылка на изображение',
        }


IngredientFormSet = modelformset_factory(
    Ingredient, 
    fields=('name', 'quantity', 'unit'), 
    labels={
        'name': 'Название ингредиента',
        'quantity': 'Количество',
        'unit': 'Единица измерения',
    },
    extra=1 
)