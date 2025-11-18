from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['musician', 'listing', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'listing__genres']
    search_fields = ['musician__username', 'listing__title', 'listing__band_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('musician', 'listing', 'status')
        }),
        ('Application Details', {
            'fields': ('message',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )