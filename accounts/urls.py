from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('musician_profile/', views.musician_profile_view, name='musician_profile'),
    path('band_profile/', views.band_profile_view, name='band_profile'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
]