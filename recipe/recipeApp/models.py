from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

# Common Timestamp Model
class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This ensures it doesn't create a separate table in the database


class Recipe(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    time_needed = models.CharField(max_length=50, default="Not specified")


    def __str__(self):
        return self.recipe_name

class Ingredient(Timestamp):
    ingredient_name = models.CharField(max_length=255)

    def __str__(self):
        return self.ingredient_name

class RecipeIngredient(Timestamp):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measure = models.CharField(max_length=50, default="Enter measurement")

    def __str__(self):
        return f"{self.recipe.recipe_name}: {self.ingredient.ingredient_name} - {self.measure}"  


class Instruction(Timestamp):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_no = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='instruction_images/', null=True, blank=True)

    def __str__(self):
        return f"Step {self.step_no} for {self.recipe.recipe_name}"

class Favorite(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')  # Prevent duplicate favorites

    def __str__(self):
        return f"{self.user.username} favorited {self.recipe.recipe_name}"
    
class Rating(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Example: 1-5 stars
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.recipe_name} {self.rating} stars"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return self.user.username