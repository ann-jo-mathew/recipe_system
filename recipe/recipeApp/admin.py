from django.contrib import admin

# Register your models here.
from .models import Recipe
from .models import Ingredient
""" from .models import RecipeIngredient """
from .models import Instruction, Category
from .models import Favorite
from .models import Rating



admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Instruction)
admin.site.register(Favorite)
admin.site.register(Rating)
