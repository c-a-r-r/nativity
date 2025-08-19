# backend/users/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ModuleViewSet, RoleViewSet, UsuarioViewSet, get_users_by_role

router = DefaultRouter()
router.register(r'modules', ModuleViewSet)
router.register(r'roles',   RoleViewSet)
router.register(r'users',   UsuarioViewSet)

urlpatterns = router.urls + [
    path('users-by-role/', get_users_by_role, name='users-by-role'),
]