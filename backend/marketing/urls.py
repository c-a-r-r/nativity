from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views_upload import ImageUploadView


router = DefaultRouter()
router.register(r'templates', views.MarketingTripTemplateViewSet)
router.register(r'template-destinations', views.TemplateDestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', ImageUploadView.as_view(), name='marketing-upload-image'),
    path('create-trip/', views.CreateMarketingTripView.as_view(), name='marketing-create-trip'),
    path('trips/<slug:slug>/', views.PublicTripView.as_view(), name='marketing-public-trip'),
path('trips/private/<slug:slug>/', views.PrivateTripView.as_view(), name='marketing-private-trip'),
]