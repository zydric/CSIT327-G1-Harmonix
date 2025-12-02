from django.urls import path
from . import views

app_name = 'invitations'

urlpatterns = [
    # Band Admin Views
    path('invite/', views.band_admin_invite_musicians, name='band_admin_invite'),
    path('send/', views.send_invitation, name='send_invitation'),
    
    # Musician Views  
    path('received/', views.musician_received_invitations, name='musician_invitations'),
    path('respond/', views.respond_to_invitation, name='respond_invitation'),

    path('sent/', views.band_sent_invites, name='band_sent_invites'),
    
    # API Endpoints
    path('listing/<int:listing_id>/', views.get_listing_details, name='listing_details'),
]