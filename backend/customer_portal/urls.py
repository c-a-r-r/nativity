from django.urls import path
from . import views

app_name = 'customer_portal'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('logout/', views.customer_logout, name='logout'),
    
    # Profile and account management
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    path('account/', views.CustomerAccountView.as_view(), name='account'),
    
    # Password management
    path('change-password/', views.change_password, name='change_password'),
    path('request-password-reset/', views.request_password_reset, name='request_password_reset'),
    path('confirm-password-reset/', views.confirm_password_reset, name='confirm_password_reset'),
    
    # Email verification
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
]
