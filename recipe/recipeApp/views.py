from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Signup View
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'recipeApp/signup.html')
# Login View
def login(request):
    if request.method == 'POST':
        form = authenticate(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')  # Redirect to homepage
    else:
        form = authenticate()
    return render(request, 'recipeApp/login.html', {'form': form})

# Logout View
def logout(request):
    logout(request)
    return redirect('index')  # Redirect to homepage after logout

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