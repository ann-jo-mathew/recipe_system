from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Ingredient, Instruction, Rating, Favorite, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
# Rename to avoid conflict
from django.contrib import messages
import logging
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, RecipeForm
from django.db.models import Avg
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
import random
import string

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
    latest_recipes = Recipe.objects.annotate(avg_rating=Avg('rating__rating')).order_by('-created_at')[:6]  # Fetch latest 6 recipes
    
    # Convert avg_rating to full_stars and empty_stars
    for recipe in latest_recipes:
        recipe.full_stars = int(recipe.avg_rating) if recipe.avg_rating else 0
        recipe.empty_stars = 5 - recipe.full_stars

    context = {
        'latest_recipes': latest_recipes,
        'user': request.user  # Include the user object in the context
    }
    return render(request, 'recipeApp/index.html', context)

"""def blog_post(request):
    return render(request, 'recipeApp/blog-post.html')

def recipe_post(request):
    return render(request, 'recipeApp/recipe-post.html')"""

def contact(request):
    return render(request, 'recipeApp/contact.html')

"""def elements(request):
    return render(request, 'recipeApp/elements.html')"""
 

def recipe_detail(request, recipe_name):
    recipe = get_object_or_404(Recipe, recipe_name=recipe_name)
    return render(request, 'recipeApp/recipe_detail.html', {'recipe': recipe})


""" def latest_recipes(request):
    latest_recipes = Recipe.objects.order_by('-created_at')[:6]  # Fetch latest 6 recipes
    print(latest_recipes)  
    return render(request, 'recipeApp/latest_recipes.html', {'latest_recipes': latest_recipes})"""

def search_recipe(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    recipes = Recipe.objects.filter(recipe_name__icontains=query)if query else []  # Case-insensitive search

    for recipe in recipes:
        # Fetch ingredients and instructions for each recipe
        recipe.ingredients = Ingredient.objects.filter(recipe=recipe)
        recipe.instructions = Instruction.objects.filter(recipe=recipe).order_by('step_no')
        ratings = Rating.objects.filter(recipe=recipe)

        # Calculate average rating
        if ratings.exists():
            recipe.average_rating = sum(r.rating for r in ratings) / ratings.count()
        else:
            recipe.average_rating = 0  # Default to 0 if no ratings

    return render(request, 'recipeApp/recipe-search-results.html', {'recipes': recipes, 'query': query})

def about(request):
    return render(request, 'recipeApp/about.html')

def best_rated_recipes(request):
    # Get the top 9 recipes based on average rating
    top_recipes = Recipe.objects.all().annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:9]

    # Convert avg_rating to full_stars and empty_stars
    for recipe in top_recipes:
        recipe.full_stars = int(recipe.avg_rating) if recipe.avg_rating else 0
        recipe.empty_stars = 5 - recipe.full_stars

    return render(request, 'recipeApp/best_recipes.html', {'top_recipes': top_recipes})

#@login_required(login_url='/login/')

def change_password(request):
    if request.method == "POST":
        username_email = request.POST['username_email']
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
         # Check if the username or email exists
        user = User.objects.filter(username=username_email).first() or User.objects.filter(email=username_email).first()
        if user:
            if new_password == confirm_password:
                user.password = make_password(new_password)  # Hash password
                user.save()
                messages.success(request, "Your password has been reset successfully! You can now login.")
                return redirect('loginuser')
            else:
                messages.error(request, "Passwords do not match. Please try again.")
        else:
            messages.error(request, "User not found. Please check your username or email.")

    return render(request, 'recipeApp/c-password.html')

def recipe_detail(request, recipe_name):
    recipe = get_object_or_404(Recipe, recipe_name=recipe_name)
    instructions = Instruction.objects.filter(recipe=recipe).order_by('step_no')
    ingredients = Ingredient.objects.filter(recipe=recipe)
    
    # Ensure user is authenticated before querying Favorite
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    else:
        is_favorited = False  # Anonymous users can't have favorites

    favorite_users = Favorite.objects.filter(recipe=recipe).values_list('user', flat=True)

    # Calculate average rating
    average_rating = Rating.objects.filter(recipe=recipe).aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, 'recipeApp/recipe_detail.html', {
        'recipe': recipe,
        'instructions': instructions,
        'ingredients': ingredients,
        'average_rating': average_rating,
        'is_favorited': is_favorited,  # Pass this to the template
        'favorite_users': favorite_users,
    })



def recipe_comments(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = Rating.objects.filter(recipe=recipe)

    user_comment = None
    if request.user.is_authenticated:
        user_comment = Rating.objects.filter(user=request.user, recipe=recipe).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('loginuser')  # Redirect to login page

        rating = request.POST.get('rating')
        comment_text = request.POST.get('comment')

        if rating and comment_text:
            if user_comment:
                user_comment.rating = int(rating)
                user_comment.comment = comment_text
                user_comment.save()
                messages.success(request, "Your rating and comment have been updated.")
            else:
                Rating.objects.create(
                    user=request.user,
                    recipe=recipe,
                    rating=int(rating),
                    comment=comment_text
                )
                messages.success(request, "Your rating and comment have been added.")

            return redirect('recipe_comments', recipe_id=recipe.id)

    return render(request, 'recipeApp/recipe_comments.html', {
        'recipe': recipe,
        'comments': comments,
        'user_comment': user_comment
    })


#recipe upload
""" @login_required """
def create_recipe(request):
    if not request.user.is_authenticated:
        return render(request, "recipeApp/create.html")

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)  # Create a recipe object but don't save yet
            recipe.user = request.user  # Assign the logged-in user
            recipe.save()  # Now save the recipe

            # Save Ingredients
            ingredients = request.POST.get("ingredients", "").split("\n")
            for ingredient in ingredients:
                if "-" in ingredient:
                    name, measure = ingredient.split("-", 1)
                    Ingredient.objects.create(
                        recipe=recipe,
                        ingredient_name=name.strip(),
                        measure=measure.strip()
                    )

            # Save Instructions
            instructions = request.POST.get("instructions", "").split("\n")
            for instruction in instructions:
                if ":" in instruction:
                    step_no, description = instruction.split(":", 1)
                    Instruction.objects.create(
                        recipe=recipe,
                        step_no=int(step_no.strip()),
                        description=description.strip()
                    )

            messages.success(request, "Recipe added successfully!")
            return redirect("recipes")  # Redirect to the recipes list page

    else:
        form = RecipeForm()

    return render(request, "recipeApp/create.html", {"form": form})
""" def create_recipe(request):
    if not request.user.is_authenticated:
        return render(request, "recipeApp/create.html")  # Show encouragement instead of redirecting

    if request.method == "POST":
        recipe_name = request.POST['recipe_name']
        time_needed = request.POST['time_needed']
        serving_portion = request.POST['serving_portion']
        image = request.FILES.get('image')

        # Create and save recipe instance
        recipe = Recipe.objects.create(
            user=request.user,
            recipe_name=recipe_name,
            time_needed=time_needed,
            serving_portion=serving_portion,
            image=image
        )

        # Save Ingredients
        ingredients = request.POST['ingredients'].split("\n")
        for ingredient in ingredients:
            if "-" in ingredient:
                name, measure = ingredient.split("-", 1)
                Ingredient.objects.create(recipe=recipe, ingredient_name=name.strip(), measure=measure.strip())

        # Save Instructions
        instructions = request.POST['instructions'].split("\n")
        for instruction in instructions:
            if ":" in instruction:
                step_no, description = instruction.split(":", 1)
                Instruction.objects.create(recipe=recipe, step_no=int(step_no.strip()), description=description.strip())

        messages.success(request, "Recipe added successfully!")
        return redirect("recipes")  # Redirect to recipes page after creation

    return render(request, "recipeApp/create.html") """
""" if request.method == "POST":
    form = RecipeForm(request.POST, request.FILES)
    if form.is_valid():
        recipe = form.save(commit=False)  # Don't save yet
        recipe.user = request.user  # Assign the logged-in user
        recipe.save()
        return redirect('recipes')  # Redirect to recipe list or another page
else:
    form = RecipeForm()

return render(request, 'recipeApp/create.html', {'form': form})
"""
def upload_recipe(request):
    return render(request, 'recipeApp/upload_recipe.html')    

def favorite_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)

        if not created:
            # If already favorited, remove from favorites
            favorite.delete()

        return redirect('recipe_detail', recipe_name=recipe.recipe_name)  # Redirect to recipe detail if logged in
    else:
        return redirect('favorites')  # Redirect to favorites page if not logged in

def favorites(request):
    favorite_recipes = Recipe.objects.filter(favorite__user=request.user) if request.user.is_authenticated else None
    return render(request, 'recipeApp/favorites.html', {'favorite_recipes': favorite_recipes})
  
def recipe_list(request):    
    recipes = Recipe.objects.all().annotate(avg_rating=Avg('rating__rating')).order_by('-created_at')
    # Convert avg_rating to full_stars and empty_stars
    for recipe in recipes:
        recipe.full_stars = int(recipe.avg_rating) if recipe.avg_rating else 0
        recipe.empty_stars = 5 - recipe.full_stars

    paginator = Paginator(recipes, 9)  
    page_number = request.GET.get('page')  
    recipes = paginator.get_page(page_number) 
    return render(request, 'recipeApp/recipes.html', {'recipes': recipes})

def about(request):
    return render(request, 'recipeApp/about.html')

def contact(request):
    return render(request, 'recipeApp/contact.html')