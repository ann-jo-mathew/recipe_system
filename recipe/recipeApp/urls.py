from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'), 
    path('recipe/<str:recipe_name>/', views.recipe_detail, name='recipe_detail'),
    path('login/', views.login_user, name='loginuser'), 
    path('signup/', views.signup, name='signup'),
    path('logout/',views.logout_user, name='logout'),
    path('passwordreset/', views.passwordreset, name='password'),
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)