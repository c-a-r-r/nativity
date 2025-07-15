from rest_framework.routers import DefaultRouter
from .views import ClientViewSet

router = DefaultRouter()
router.register(r'contacts', ClientViewSet, basename='contacts')

urlpatterns = router.urls