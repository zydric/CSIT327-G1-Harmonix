from django.contrib import admin
from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['band_admin', 'musician', 'listing', 'status', 'has_message', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['band_admin__username', 'musician__username', 'listing__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_message(self, obj):
        return bool(obj.message)
    has_message.boolean = True
    has_message.short_description = 'Has Message'
