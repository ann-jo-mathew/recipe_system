from django import forms
from .models import UserProfile, Rating, Recipe, Ingredient, Instruction

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone_number', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(widget=forms.Textarea, help_text="Enter one per line as 'name - measure'")
    instructions = forms.CharField(widget=forms.Textarea, help_text="Enter one per line as 'Step No: Description'")

    class Meta:
        model = Recipe
        fields = ['recipe_name', 'image', 'time_needed', 'serving_portion']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'measure']

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['step_no', 'description']