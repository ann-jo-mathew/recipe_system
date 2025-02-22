from django.shortcuts import render, redirect
from .models import Recipe

def index(request):
    recipes = Recipe.objects.all()  # Fetch all recipes
    return render(request, 'recipeApp/index.html')