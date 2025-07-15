from rest_framework import serializers
from .models import Quote, DestinationGroup, Destination, ItineraryCity

class QuoteSerializer(serializers.ModelSerializer):
    workflow_status_nombre = serializers.CharField(source='workflow_status_rel.nombre', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    departure_city_display = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    destination_group_nombre = serializers.CharField(source='destination_group.nombre', read_only=True)
    destination_nombre = serializers.CharField(source='destination.nombre', read_only=True)
    departure_city_cost = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = '__all__'  # or list all fields explicitly, plus the above

    def get_departure_city_display(self, obj):
        city = getattr(obj, 'departure_city_id', None)
        if city:
            return f"{city.city_code} - {city.city}"
        return ""

    def get_user_full_name(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return ""
    
    def get_client_name(self, obj):
        client = getattr(obj, 'client', None)
        if client:
            return f"{getattr(client, 'first_name', '')} {getattr(client, 'last_name', '')}".strip()
        return ""
    
    def get_departure_city_cost(self, obj):
        city = getattr(obj, 'departure_city_id', None)
        if city and hasattr(city, 'cost'):
            return city.cost
        return 0
    
class DestinationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationGroup
        fields = ['id', 'nombre']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'nombre']

class ItineraryCitySerializer(serializers.ModelSerializer):
    short_display = serializers.SerializerMethodField()

    class Meta:
        model = ItineraryCity
        fields = '__all__'

    def get_short_display(self, obj):
        return f"{obj.city_code} - {obj.city} + (${obj.cost})"
