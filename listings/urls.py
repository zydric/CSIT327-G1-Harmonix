from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listings_view, name='feed'),
    path('create/', views.create_listing, name='create'),
    path('<int:pk>/', views.listing_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_listing, name='edit'),
    path('<int:pk>/delete/', views.delete_listing, name='delete'),
]