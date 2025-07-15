from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'templates', views.WebsiteTemplateViewSet)
router.register(r'trips', views.TripInstanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('trips/public/<slug:slug>/', views.TripPublicView.as_view(), name='trip-public'),
    path('trips/private/<uuid:token>/', views.TripPrivateView.as_view(), name='trip-private'),
    path('trips/<slug:slug>/register/', views.TripRegistrationView.as_view(), name='trip-register'),

    path('quotes/<int:quote_id>/create-trip/', views.QuoteTripCreateView.as_view(), name='quote-create-trip'),
]