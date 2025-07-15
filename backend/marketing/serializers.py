from rest_framework import serializers
from .models import TripTemplate, Trip, TripRegistration

class TripTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripTemplate
        fields = "__all__"

class TripSerializer(serializers.ModelSerializer):
    template = TripTemplateSerializer(read_only=True)
    quote_data = serializers.SerializerMethodField()
    
    def get_quote_data(self, obj):
        quote = obj.quote
        if quote:
            return {
                'id': quote.id,
                'group_name': quote.group_name,
                'church_name': quote.church_name,
                'leader_name': quote.leader_name
            }
        return None
    
    class Meta:
        model = Trip
        fields = (
            "id", "slug", "departure_date", "arrival_date", "price",
            "template", "trip_name", "church_name", "spiritual_director",
            "quote_id", "quote_data"
        )

class TripDetailSerializer(serializers.ModelSerializer):
    template = TripTemplateSerializer(read_only=True)
    final_title = serializers.ReadOnlyField()
    final_description = serializers.ReadOnlyField()
    final_itinerary = serializers.ReadOnlyField()
    final_includes = serializers.ReadOnlyField()
    final_excludes = serializers.ReadOnlyField()
    quote_data = serializers.SerializerMethodField()
    
    def get_quote_data(self, obj):
        quote = obj.quote
        if quote:
            return {
                'id': quote.id,
                'group_name': quote.group_name,
                'church_name': quote.church_name,
                'leader_name': quote.leader_name
            }
        return None
    
    class Meta:
        model = Trip
        fields = [
            'id', 'slug', 'trip_name', 'church_name', 'spiritual_director',
            'departure_date', 'arrival_date', 'price', 'is_published',
            'final_title', 'final_description', 'final_itinerary', 
            'final_includes', 'final_excludes', 'template', 'quote_data'
        ]

class TripPrivateSerializer(TripDetailSerializer):
    contact = serializers.SerializerMethodField()
    
    def get_contact(self, obj):
        token = self.context.get('token')
        if token:
            private_access = obj.private_tokens.filter(token=token).first()
            if private_access and private_access.contact:
                contact = private_access.contact
                return {
                    'name': f"{contact.first_name} {contact.last_name}",
                    'email': contact.email,
                    'phone': contact.phone
                }
        return None
    
    class Meta(TripDetailSerializer.Meta):
        fields = TripDetailSerializer.Meta.fields + ['contact']

class TripRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRegistration
        fields = '__all__'

# Aliases for backward compatibility
WebsiteTemplateSerializer = TripTemplateSerializer
TripInstanceSerializer = TripSerializer