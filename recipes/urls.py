from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_recipes, name='page_recipes'),
    path('send_recipes/', views.send_recipes, name='send_recipes'),
    path('<int:recipe_id>/', views.detail_recipes, name='detail_recipes'),
]
