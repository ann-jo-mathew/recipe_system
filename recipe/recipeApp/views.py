from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    # Food.objects
    return render(request, 'recipeApp/index.html')

def about(request):
    return render(request, 'recipeApp/about.html')

def blog_post(request):
    return render(request, 'recipeApp/blog-post.html')

def recipe_post(request):
    return render(request, 'recipeApp/recipe-post.html')

def contact(request):
    return render(request, 'recipeApp/contact.html')

def elements(request):
    return render(request, 'recipeApp/elements.html')