from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    time_needed = models.CharField(max_length=50, default="Not specified")


    def __str__(self):
        return self.recipe_name

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)

    def __str__(self):
        return self.ingredient_name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measure = models.CharField(max_length=50, default="Enter measurement")

    def __str__(self):
        return self.ingredient.ingredient_name


class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_no = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='instruction_images/', null=True, blank=True)

    def __str__(self):
        return f"Step {self.step_no} for {self.recipe.recipe_name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} favorited {self.recipe.recipe_name}"
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Example: 1-5 stars
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.recipe_name} {self.rating} stars"