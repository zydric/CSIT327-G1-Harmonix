from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:pk>/', views.apply_to_listing, name='apply'),
    path('status/<int:pk>/', views.update_application_status, name='update_status'),
    path('withdraw/<int:pk>/', views.withdraw_application, name='withdraw'),
    path('my-applications/', views.my_applications, name='my_applications'),
]