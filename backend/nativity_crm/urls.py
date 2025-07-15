# backend/nativity_crm/urls.py
from django.contrib import admin
from users.views import current_user
from django.urls import path, include
from marketing.views import TripInstanceView, TemplateList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # -- auth endpoints:
    path('api/auth/login/',   TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),

    # -- your other API routers:
    path('api/', include('users.urls')),   # modules/roles/users
    path('api/', include('quotes.urls')),  # quotes
    path('api/', include('contacts.urls')),  # contacts

    path('api/current-user/', current_user, name='current-user'),

    # # -- marketing module:
    path('admin/', admin.site.urls),
    path('api/quotes/', include('quotes.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/marketing/', include('marketing.urls')),

]