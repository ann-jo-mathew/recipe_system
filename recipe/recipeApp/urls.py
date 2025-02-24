from django.urls import path
from . import views  

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<str:recipe_name>/', views.recipe_detail, name='recipe_detail'),

]