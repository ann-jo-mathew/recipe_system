from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe

def index(request):
    latest_recipes = Recipe.objects.order_by('-created_at')[:6]  # Fetch latest 6 recipes
    return render(request, 'recipeApp/index.html', {'latest_recipes': latest_recipes})

""" def index(request):
    recipes = Recipe.objects.all()  # Fetch all recipes
    return render(request, 'recipeApp/index.html')
     """
""" def about(request):
    return render(request, 'recipeApp/about.html')

def blog_post(request):
    return render(request, 'recipeApp/blog-post.html')

def recipe_post(request):
    return render(request, 'recipeApp/recipe-post.html')

def contact(request):
    return render(request, 'recipeApp/contact.html')

def elements(request):
    return render(request, 'recipeApp/elements.html')
 """
def demo(request):
    recipes = Recipe.objects.all()  # Fetch all recipes
    return render(request, 'recipeApp/demo.html',{'recipes':recipes})

""" def latest_recipes(request):
    latest_recipes = Recipe.objects.order_by('-created_at')[:6]  # Fetch latest 6 recipes
    print(latest_recipes)  
    return render(request, 'recipeApp/latest_recipes.html', {'latest_recipes': latest_recipes})

def recipe_detail(request, recipe_name):
    recipe = get_object_or_404(Recipe, recipe_name=recipe_name)
    return render(request, 'recipeApp/recipe_detail.html', {'recipe': recipe})
     """

def recipe_detail(request, recipe_name):
    recipe = get_object_or_404(Recipe, recipe_name=recipe_name)
    latest_recipes = Recipe.objects.order_by('-created_at')[:6]  # Fetch latest 6 recipes
    return render(request, 'recipeApp/index.html', {
        'recipe': recipe,
        'latest_recipes': latest_recipes
    })