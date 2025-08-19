"""
Trip Registration URL Configuration
"""
from django.urls import path
from . import views

app_name = 'trip_registration'

urlpatterns = [
    # Lookup endpoints
    path('countries/', views.get_countries, name='get_countries'),
    path('pilgrimage/<int:pilgrimage_id>/', views.get_pilgrimage, name='get_pilgrimage'),
    
    # Registration flow
    path('submit/', views.submit_registration, name='submit_registration'),
    path('payment/process/', views.process_payment, name='process_payment'),
    path('status/<str:session_id>/', views.check_registration_status, name='check_registration_status'),
    
    # Maintenance
    path('cleanup/', views.cleanup_expired_registrations, name='cleanup_expired_registrations'),
]
