from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Предназначен для административных функций, в частности, здесь производится регистрация моделей, которые
# используются в интерфейсе администратора

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('phone_number', 'email', 'name', 'is_staff', 'is_active',)
    list_filter = ('phone_number', 'email', 'name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('phone_number', 'email', 'name',)
    ordering = ('phone_number',)

admin.site.register(User, CustomUserAdmin)