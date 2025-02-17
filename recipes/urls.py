from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_recipes, name='page_recipes'),
    path('create_recipes/', views.create_recipes, name='create_recipes'),
    path('<int:recipe_id>/', views.detail_recipes, name='detail_recipes'),
    path('shopping/<int:recipe_id>/', views.shopping, name='shopping'),
    path('shopping_list', views.shopping_list, name='shopping_list'),
    path('clear_shopping_cart/', views.clear_shopping_cart, name='clear_shopping_cart'),
    path('clear_one_shopping_cart/<int:recipe_id>/', views.clear_one_shopping_cart, name='clear_one_shopping_cart'),
]
