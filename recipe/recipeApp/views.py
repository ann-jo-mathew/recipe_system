from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout  # Rename to avoid conflict
from django.contrib import messages
import logging
from django.contrib.auth import get_user_model  # ✅ Add this import
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm



logger = logging.getLogger(__name__)

# Signup View
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "recipeApp/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "recipeApp/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "recipeApp/signup.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('loginuser')

    return render(request, 'recipeApp/signup.html')
# Login View
def login_user(request):
    if request.method == 'POST':
        login_input = request.POST.get('username')  # Can be username or email
        password = request.POST.get('password')

        User = get_user_model()  # Get Django's User model

        try:
            # Check if input is an email
            user = User.objects.get(email=login_input)
            username = user.username  # Retrieve the actual username
        except User.DoesNotExist:
            username = login_input  # Assume it's a username

        # Authenticate using username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')  
        else:
            messages.error(request, "Invalid email or password")
            return redirect('loginuser')

    return render(request, 'recipeApp/login.html')

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)  # Ensures profile exists
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Reload the same page after saving

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'recipeApp/user_profile.html', {'profile': profile, 'form': form})

# Logout View
def logout_user(request):
    auth_logout(request)
    messages.success(request, "Thanks for spending some quality time with the website today. Log in again if needed.")
    return redirect('index')  # Redirect to homepage
# Index View
def index(request):
    latest_recipes = Recipe.objects.order_by('-created_at')[:6]  # Fetch latest 6 recipes
    context = {
        'latest_recipes': latest_recipes,
        'user': request.user  # Include the user object in the context
    }
    return render(request, 'recipeApp/index.html', context)

""" def index(request):
    recipes = Recipe.objects.all()  # Fetch all recipes
    return render(request, 'recipeApp/index.html')
     """

"""def blog_post(request):
    return render(request, 'recipeApp/blog-post.html')

def recipe_post(request):
    return render(request, 'recipeApp/recipe-post.html')"""

def contact(request):
    return render(request, 'recipeApp/contact.html')

"""def elements(request):
    return render(request, 'recipeApp/elements.html')"""
 

""" def latest_recipes(request):
    latest_recipes = Recipe.objects.order_by('-created_at')[:6]  # Fetch latest 6 recipes
    print(latest_recipes)  
    return render(request, 'recipeApp/latest_recipes.html', {'latest_recipes': latest_recipes})"""

"""def recipe_detail(request, recipe_name):
    recipe = get_object_or_404(Recipe, recipe_name=recipe_name)
    return render(request, 'recipeApp/recipe_detail.html', {'recipe': recipe})  # ✅ Correct template"""

def about(request):
    return render(request, 'recipeApp/about.html')


def passwordreset(request):
    return render(request, 'recipeApp/passwordreset.html')

def recipe_detail(request, recipe_name):
    recipe = get_object_or_404(Recipe, recipe_name=recipe_name)
    latest_recipes = Recipe.objects.order_by('-created_at')[:6]  # Fetch latest 6 recipes
    return render(request, 'recipeApp/index.html', {
        'recipe': recipe,
        'latest_recipes': latest_recipes
    })
def upload_recipe(request):
    return render(request, 'recipeApp/upload_recipe.html')