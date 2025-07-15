# backend/users/urls.py

from rest_framework.routers import DefaultRouter
from .views import ModuleViewSet, RoleViewSet, UsuarioViewSet

router = DefaultRouter()
router.register(r'modules', ModuleViewSet)
router.register(r'roles',   RoleViewSet)
router.register(r'users',   UsuarioViewSet)

urlpatterns = router.urls