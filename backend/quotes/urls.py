from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import QuoteViewSet, destination_group_list, destination_list, itinerary_city_list
from marketing.views import QuoteTripCreateView

router = DefaultRouter()
router.register(r'quotes', QuoteViewSet, basename='quote')

urlpatterns = router.urls + [
    path('destination-groups/', destination_group_list, name='destination-group-list'),
    path('destinations/', destination_list, name='destination-list'),
    path('itinerary-cities/', itinerary_city_list, name='itinerary-city-list'),

    #marketing
    path('quotes/<int:quote_id>/create-trip/', QuoteTripCreateView.as_view(), name='quote-create-trip'),
]