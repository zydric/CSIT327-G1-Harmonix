from django.urls import path
from . import views

app_name = 'invitations'

urlpatterns = [
    path('', views.invites_page, name='invites'),
    path('send/', views.send_invitation, name='send_invitation'),
]