from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('usuario', 'email', 'nombre', 'is_staff', 'is_active')
    search_fields = ('usuario', 'email')
    ordering = ('usuario',)

admin.site.register(Usuario, UsuarioAdmin)
