from django import forms
from .models import UserProfile, Rating, Recipe, Ingredient, Instruction, Category

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'address', 'phone_number', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        profile.user.username = self.cleaned_data['username']
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(
        widget=forms.Textarea, 
        help_text="Enter one per line as 'name - measure'"
    )
    instructions = forms.CharField(
        widget=forms.Textarea, 
        help_text="Enter one per line as 'Step No: Description'"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        help_text="Select a category for this recipe",
        empty_label="Choose category"
    )

    class Meta:
        model = Recipe
        fields = ['recipe_name', 'image', 'time_needed', 'serving_portion', 'category']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'measure']

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['step_no', 'description']