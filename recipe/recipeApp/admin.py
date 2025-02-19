from django.contrib import admin

# Register your models here.
from .models import Recipe
from .models import Ingredient
from .models import RecipeIngredient
from .models import Instruction


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Instruction)
