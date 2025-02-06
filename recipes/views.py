from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, Ingredient, ShoppingCart
from django.core.paginator import Paginator
import nltk
from .forms import RecipeForm, IngredientFormSet
import re


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

        return redirect('page_recipes')
    else:
        recipe_form = RecipeForm()
        ingredient_formset = IngredientFormSet(queryset=Ingredient.objects.none())

    return render(request, 'recipes/create_recipes.html', {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset})


def page_recipes(request):
    query = request.GET.get('q', '')
    recipes_list = Recipe.objects.filter(name__icontains=query).order_by('name') if query else Recipe.objects.order_by('name')
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

def in_decimal(x):
    if "/" in x:
        numerator, denominator = map(float, x.split("/"))
        return str(numerator / denominator)
    return x

def one_num(x):
    if x.count('.') > 1 or x.count(',') > 1 or '-' in x or \
       re.search(r'[^\d\s.,-/]', x):
        match = re.search(r'(\d+(?:[.,]\d+)?)', x)
        if match:
            return str(match.group(1).replace(',', '.'))
    if ',' in x:
        return str(x.replace(',', '.'))
    if x == "":
        return str(0)
    return x


def shopping(request, recipe_id):
    user = request.user

    if request.method == 'POST':
        
        ingredients = Ingredient.objects.filter(recipe_id=recipe_id)

        for ingredient in ingredients:
        
            cart_item = ShoppingCart.objects.filter(
                user_id=user,
                ingredient_id__name=ingredient.name,  
                unit=ingredient.unit  
            ).first()

            if cart_item:
                    cart_item_quantity = in_decimal(cart_item.quantity)
                    ingredient_quantity = in_decimal(ingredient.quantity) 
                    cart_item_quantity = one_num(cart_item_quantity)
                    ingredient_quantity = one_num(ingredient_quantity)
                    
                    cart_item.quantity = str(float(cart_item_quantity) + float(ingredient_quantity))
                    cart_item.save()
            else:
                
                ShoppingCart.objects.create(
                    user_id=user,
                    ingredient_id=ingredient,  
                    quantity=ingredient.quantity,
                    unit=ingredient.unit
                )

        return redirect('page_recipes')
    
    
def shopping_list(request):
    user = request.user.id
    shopping_items = ShoppingCart.objects.filter(user_id=user)

    recipes_dict = {}

    # Создаем список всех ингредиентов
    all_ingredients = []

    for item in shopping_items:
        recipe_name = item.ingredient_id.recipe_id.name
        recipe_image = item.ingredient_id.recipe_id.image_url

        if recipe_name not in recipes_dict:
            recipes_dict[recipe_name] = {
                'image_url': recipe_image,
                'ingredients': []
            }

        ingredient_data = {
            'name': item.ingredient_id.name,
            'quantity': item.quantity,
            'unit': item.unit,
            'recipe_name': recipe_name  
        }

        recipes_dict[recipe_name]['ingredients'].append(ingredient_data)
        all_ingredients.append(ingredient_data)

    for recipe_data in recipes_dict.values():
        recipe_data['ingredients'].sort(key=lambda x: x['name'])

    all_ingredients.sort(key=lambda x: x['name'])

    return render(request, 'recipes/shopping_list.html', {
        'user': user,
        'recipes': recipes_dict.items(),  
        'all_ingredients': all_ingredients  
    })

def clear_shopping_cart(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            ShoppingCart.objects.filter(user_id=user.id).delete()
        return redirect('shopping_list')

