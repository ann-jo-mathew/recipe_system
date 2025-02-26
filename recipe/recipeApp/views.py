from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout  # Rename to avoid conflict
from django.contrib import messages
import logging
from django.contrib.auth import get_user_model  # ✅ Add this import
from django.contrib.auth.decorators import login_required


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

def recipe_detail(request, recipe_name):
    recipe = get_object_or_404(Recipe, recipe_name=recipe_name)
    return render(request, 'recipeApp/recipe_detail.html', {'recipe': recipe})



def passwordreset(request):
    return render(request, 'recipeApp/passwordreset.html')
