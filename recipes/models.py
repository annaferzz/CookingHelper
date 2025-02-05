from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instruction = models.TextField()
    image_url = models.URLField()

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=30, default='0')
    unit = models.CharField(max_length=50, default='гр.')

class ShoppingCart(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=30, default='0')
    unit = models.CharField(max_length=50, default='гр.')