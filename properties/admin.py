from django.contrib import admin
from .models import Property, PropertyImage, Amenity, Favorite


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class AmenityInline(admin.TabularInline):
    model = Amenity
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'listing_type', 'price', 'location', 'is_featured', 'owner', 'created_at')
    list_filter = ('type', 'listing_type', 'is_featured')
    search_fields = ('title', 'location', 'description')
    ordering = ('-created_at',)
    inlines = [PropertyImageInline, AmenityInline]
    list_editable = ('is_featured',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at')
    list_filter = ('created_at',)
