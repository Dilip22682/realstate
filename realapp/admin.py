from django.contrib import admin
from .models import Property, Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['user', 'property', 'date', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['user__username', 'property__title']
    list_editable = ['status']   # change status directly from admin list

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'location', 'price', 'property_type']
    list_filter   = ['property_type']
    search_fields = ['title', 'location']