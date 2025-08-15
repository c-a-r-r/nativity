from rest_framework import serializers
from .models import MarketingTripTemplate, TemplateDestination, MarketingTrip

class MarketingTripTemplateSerializer(serializers.ModelSerializer):
    destination_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MarketingTripTemplate
        fields = "__all__"
        extra_fields = ['destination_name']

    def get_destination_name(self, obj):
        return obj.destination.name if obj.destination else None

class TemplateDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateDestination
        fields = ['id', 'name', 'created_at']

class MarketingTripSerializer(serializers.ModelSerializer):
    destination = serializers.SerializerMethodField()
    quote = serializers.SerializerMethodField()
    leader_name = serializers.SerializerMethodField()
    itinerary = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    brochure = serializers.SerializerMethodField()
    video_link = serializers.SerializerMethodField()
    trip_includes = serializers.SerializerMethodField()
    trip_not_includes = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    departure_city = serializers.SerializerMethodField()
    
    class Meta:
        model = MarketingTrip
        fields = '__all__'
    
    def get_destination(self, obj):
        """Get destination from the template"""
        if obj.template and obj.template.destination:
            return {
                'name': obj.template.destination.name,
                'id': obj.template.destination.id
            }
        return None
    
    def get_quote(self, obj):
        """Get essential quote data"""
        if obj.quote:
            departure_city_name = ''
            if obj.quote.departure_city_id:
                # Get just the city name from the ItineraryCity object
                departure_city_name = obj.quote.departure_city_id.city or ''
            
            return {
                'departure_city': departure_city_name,
                'id': obj.quote.id
            }
        return None
    
    def get_leader_name(self, obj):
        """Get leader name from quote or spiritual_director field"""
        if obj.quote and hasattr(obj.quote, 'leader_name') and obj.quote.leader_name:
            return obj.quote.leader_name
        return getattr(obj, 'spiritual_director', '') or ''
    
    def get_itinerary(self, obj):
        """Get itinerary from MarketingTrip instance or fallback to template"""
        # First try to get from the MarketingTrip instance
        if obj.itinerary and len(obj.itinerary) > 0:
            # If it's a string, parse it as JSON
            if isinstance(obj.itinerary, str):
                try:
                    import json
                    return json.loads(obj.itinerary)
                except (json.JSONDecodeError, ValueError):
                    pass
            return obj.itinerary
        # Fallback to template itinerary if available
        if obj.template and obj.template.itinerary and len(obj.template.itinerary) > 0:
            return obj.template.itinerary
        return []
    
    def get_gallery(self, obj):
        """Get gallery from template since MarketingTrip doesn't have gallery field"""
        # First check if MarketingTrip has gallery (might be stored as JSON string)
        if hasattr(obj, 'gallery') and obj.gallery:
            if isinstance(obj.gallery, str):
                try:
                    import json
                    return json.loads(obj.gallery)
                except (json.JSONDecodeError, ValueError):
                    pass
            elif isinstance(obj.gallery, list):
                return obj.gallery
        
        # Fallback to template gallery
        if obj.template and obj.template.gallery and len(obj.template.gallery) > 0:
            return obj.template.gallery
        return []
    
    def get_brochure(self, obj):
        """Get brochure URL from MarketingTrip or fallback to template"""
        if obj.brochure:
            return obj.brochure
        if obj.template and obj.template.brochure_link:
            return obj.template.brochure_link
        return ''
    
    def get_video_link(self, obj):
        """Get video link from MarketingTrip or fallback to template"""
        if obj.video_link:
            return obj.video_link
        if obj.template and obj.template.video_link:
            return obj.template.video_link
        return ''
    
    def get_trip_includes(self, obj):
        """Get trip includes from MarketingTrip or Quote only"""
        # First check MarketingTrip
        if hasattr(obj, 'trip_includes') and obj.trip_includes and obj.trip_includes.strip():
            return obj.trip_includes
        # Then check Quote
        if obj.quote and hasattr(obj.quote, 'trip_includes') and obj.quote.trip_includes and obj.quote.trip_includes.strip():
            return obj.quote.trip_includes
        # Return empty string if no data found
        return ''
    
    def get_trip_not_includes(self, obj):
        """Get trip not includes from MarketingTrip or Quote only"""
        # First check MarketingTrip
        if hasattr(obj, 'trip_not_includes') and obj.trip_not_includes and obj.trip_not_includes.strip():
            return obj.trip_not_includes
        # Then check Quote (note: field name is 'trip_not_include' in Quote model)
        if obj.quote and hasattr(obj.quote, 'trip_not_include') and obj.quote.trip_not_include and obj.quote.trip_not_include.strip():
            return obj.quote.trip_not_include
        # Return empty string if no data found
        return ''
    
    def get_total_cost(self, obj):
        """Get total cost from MarketingTrip or fallback to quote"""
        if obj.total_cost:
            return str(obj.total_cost)
        if obj.quote and hasattr(obj.quote, 'total_cost') and obj.quote.total_cost:
            return str(obj.quote.total_cost)
        return ''
    
    def get_departure_city(self, obj):
        """Get departure city from quote"""
        if obj.quote and obj.quote.departure_city_id and obj.quote.departure_city_id.city:
            return obj.quote.departure_city_id.city
        return ''