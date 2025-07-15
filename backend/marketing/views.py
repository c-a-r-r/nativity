from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import TripTemplate, Trip, PrivateAccessToken, TripRegistration
from .serializers import (
    TripTemplateSerializer, 
    TripSerializer, 
    TripDetailSerializer, 
    TripPrivateSerializer,
    TripRegistrationSerializer
)

# Create aliases for backward compatibility
WebsiteTemplate = TripTemplate
TripInstance = Trip
WebsiteTemplateSerializer = TripTemplateSerializer
TripInstanceSerializer = TripSerializer

class WebsiteTemplateViewSet(viewsets.ModelViewSet):
    queryset = TripTemplate.objects.filter(is_active=True)
    serializer_class = TripTemplateSerializer
    permission_classes = [IsAuthenticated]  # ADD THIS LINE - it was missing!
    
    def get_queryset(self):
        queryset = super().get_queryset()
        destination = self.request.query_params.get('destination')
        duration = self.request.query_params.get('duration')
        
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if duration:
            queryset = queryset.filter(duration_days=duration)
            
        return queryset.order_by('destination', 'duration_days')

class TripInstanceViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

class QuoteTripCreateView(APIView):
    """Create a trip from a quote using a template"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, quote_id):
        from quotes.models import Quote
        
        quote = get_object_or_404(Quote, id=quote_id)
        template_id = request.data.get('template_id')
        
        if not template_id:
            return Response({'error': 'Template ID required'}, status=400)
        
        try:
            trip = quote.create_trip_from_template(template_id)
            
            # Get the private token
            private_token = trip.private_tokens.first()
            
            # Generate complete URLs
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            public_url = f"{frontend_url}/trips/{trip.slug}"
            private_url = f"{frontend_url}/trips/private/{private_token.token}" if private_token else None
            
            return Response({
                'message': 'Trip created successfully',
                'trip_id': trip.id,
                'trip_slug': trip.slug,
                'trip_name': trip.trip_name,
                'slug': trip.slug,
                'private_token': private_token.token if private_token else None,
                'is_published': trip.is_published,
                'public_url': public_url,
                'private_url': private_url,
            }, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class TripPublicView(APIView):
    def get(self, request, slug):
        trip = get_object_or_404(Trip, slug=slug, is_published=True)
        serializer = TripDetailSerializer(trip)
        return Response(serializer.data)

class TripPrivateView(APIView):
    def get(self, request, token):
        private_access = get_object_or_404(PrivateAccessToken, token=token)
        trip = private_access.trip
        serializer = TripPrivateSerializer(trip, context={'token': token})
        return Response(serializer.data)

class TripRegistrationView(APIView):
    def post(self, request, slug):
        trip = get_object_or_404(Trip, slug=slug, is_published=True)
        
        data = request.data.copy()
        data['trip'] = trip.id
        
        serializer = TripRegistrationSerializer(data=data)
        if serializer.is_valid():
            registration = serializer.save()
            return Response({
                'message': 'Registration successful',
                'registration_id': registration.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Legacy view names for compatibility
TripInstanceView = TripPublicView
TemplateList = WebsiteTemplateViewSet