from django.urls import path
from . import views

urlpatterns = [
    path('parse-recipes/', views.parse_recipes, name='parse_recipes'),
]
