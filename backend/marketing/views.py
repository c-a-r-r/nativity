# --- Public Trip View ---
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MarketingTripTemplate


from .models import MarketingTrip
from .serializers import MarketingTripSerializer

class PublicTripView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, slug):
        trip = MarketingTrip.objects.filter(slug=slug).first()
        if not trip:
            return Response({'error': 'Trip not found'}, status=404)
        serializer = MarketingTripSerializer(trip)
        return Response({
            'slug': slug,
            'trip': serializer.data,
        })

# --- Private Trip View ---
class PrivateTripView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, slug):
        trip = MarketingTrip.objects.filter(slug=slug).first()
        if not trip:
            return Response({'error': 'Trip not found'}, status=404)
        serializer = MarketingTripSerializer(trip)
        return Response({
            'slug': slug,
            'trip': serializer.data,
        })
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings


from .models import MarketingTripTemplate, TemplateDestination
from .serializers import MarketingTripTemplateSerializer, TemplateDestinationSerializer

# --- CRUD ViewSet for MarketingTripTemplate ---
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class MarketingTripTemplateViewSet(viewsets.ModelViewSet):
    queryset = MarketingTripTemplate.objects.all()
    serializer_class = MarketingTripTemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ...existing code...

class TemplateDestinationViewSet(viewsets.ModelViewSet):
    queryset = TemplateDestination.objects.all()
    serializer_class = TemplateDestinationSerializer


# --- Create Marketing Trip API ---
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import MarketingTripTemplate
from .serializers import MarketingTripTemplateSerializer

class CreateMarketingTripView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Expecting template_id and quote_id in request.data
        template_id = request.data.get('template_id')
        quote_id = request.data.get('quote_id')
        if not template_id or not quote_id:
            return Response({'error': 'template_id and quote_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        template = MarketingTripTemplate.objects.filter(id=template_id).first()
        if not template:
            return Response({'error': 'Template not found'}, status=status.HTTP_404_NOT_FOUND)
        from quotes.models import Quote
        quote = Quote.objects.filter(id=quote_id).first()
        if not quote:
            return Response({'error': 'Quote not found'}, status=status.HTTP_404_NOT_FOUND)
        import uuid
        slug = f"trip-{template_id}-{uuid.uuid4().hex[:8]}"
        # Create the MarketingTrip record
        trip = MarketingTrip.objects.create(
            quote=quote,
            template=template,
            trip_title=template.trip_title,
            promo_text=getattr(template, 'promo_text', ''),
            hero_image=template.hero_image,
            itinerary=template.itinerary,
            departure_date=getattr(quote, 'departure_date', None),
            arrival_date=getattr(quote, 'arrival_date', None),
            total_cost=getattr(quote, 'total_cost', None),
            departure_city=getattr(quote, 'departure_city', ''),
            trip_includes=getattr(quote, 'trip_includes', ''),
            trip_not_includes=getattr(quote, 'trip_not_includes', ''),
            spiritual_director=getattr(quote, 'spiritual_director', ''),
            brochure=getattr(quote, 'brochure', ''),
            video_link=getattr(quote, 'video_link', ''),
            contact_info=getattr(quote, 'contact_info', ''),
            slug=slug,
            is_published=True
        )
        from .serializers import MarketingTripSerializer
        serializer = MarketingTripSerializer(trip)
        public_link = f"/marketing/trips/{slug}"
        private_link = f"/marketing/trips/private/{slug}"
        return Response({
            'trip': serializer.data,
            'public_link': public_link,
            'private_link': private_link,
            'slug': slug,
        }, status=status.HTTP_201_CREATED)