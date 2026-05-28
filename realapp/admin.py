from django.contrib import admin
from .models import Property, Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display       = ['id', 'user', 'property', 'name', 'phone', 'date', 'status', 'created_at']
    list_display_links = ['id', 'user']   # ✅ these are the clickable links
    list_editable      = ['status']       # ✅ now works without conflict
    list_filter        = ['status', 'date']
    search_fields      = ['user__username', 'property__title', 'name', 'phone']
    readonly_fields    = ['created_at']
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'location', 'price', 'property_type']
    list_filter   = ['property_type']
    search_fields = ['title', 'location']