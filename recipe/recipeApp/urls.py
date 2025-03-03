from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import search_recipe
#from .views import recipe_detail, recipe_comments, favorite_recipe, favorites, change_password, recipe_list


urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.recipe_list, name='recipes'), 
    path('login/', views.login_user, name='loginuser'), 
    path('signup/', views.signup, name='signup'),
    path('logout/',views.logout_user, name='logout'),
    path('change-password/', views.change_password, name="changepassword"),
    path('profile/', views.user_profile, name='user_profile'),
    path('about/', views.about, name='about'),
    path('upload/', views.upload_recipe, name='upload_recipe'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_recipe, name='search_recipe'),
    path('favorites/', views.favorites, name='favorites'),
    path('recipe/<int:recipe_id>/favorite/', views.favorite_recipe, name='favorite_recipe'),
    path('recipe/<str:recipe_name>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/comments/', views.recipe_comments, name='recipe_comments'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
     path('create/', views.create_recipe, name='create_recipe'),
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)