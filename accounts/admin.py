from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_agent', 'is_staff', 'created_at')
    list_filter = ('is_agent', 'is_staff', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('-created_at',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Hector25 Info', {'fields': ('name', 'avatar', 'phone', 'bio', 'is_agent')}),
    )
