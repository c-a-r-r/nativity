from rest_framework import serializers
from .models import Quote, DestinationGroup, Destination, ItineraryCity
from users.models import Usuario

class QuoteSerializer(serializers.ModelSerializer):
    workflow_status_nombre = serializers.CharField(source='workflow_status_rel.nombre', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    departure_city_display = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    destination_group_nombre = serializers.CharField(source='destination_group.nombre', read_only=True)
    destination_nombre = serializers.CharField(source='destination.nombre', read_only=True)
    departure_city_cost = serializers.SerializerMethodField()
    
    # Client contact information fields
    contact_phone = serializers.SerializerMethodField()
    contact_email = serializers.SerializerMethodField()
    contact_email_2 = serializers.SerializerMethodField()
    contact_email_3 = serializers.SerializerMethodField()
    
    # Account Manager and Sales Agent names
    account_manager_name = serializers.SerializerMethodField()
    sales_agent_name = serializers.SerializerMethodField()
    assigned_user_name = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = '__all__'
        # Ensure these fields are writable
        extra_kwargs = {
            'marketing_public_link': {'required': False, 'read_only': False},
            'marketing_private_link': {'required': False, 'read_only': False},
        }

    def get_departure_city_display(self, obj):
        city = getattr(obj, 'departure_city_id', None)
        if city:
            cost_display = f"(${city.cost})" if hasattr(city, 'cost') and city.cost else ""
            return f"{city.city_code} - {city.city} + {cost_display}".replace(" + ()", "").strip()
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
    
    def get_contact_phone(self, obj):
        client = getattr(obj, 'client', None)
        if client:
            return getattr(client, 'phone', None)
        return ""
    
    def get_contact_email(self, obj):
        client = getattr(obj, 'client', None)
        if client:
            return getattr(client, 'email', None)
        return ""
    
    def get_contact_email_2(self, obj):
        client = getattr(obj, 'client', None)
        if client:
            return getattr(client, 'email2', None)
        return ""
    
    def get_contact_email_3(self, obj):
        client = getattr(obj, 'client', None)
        if client:
            return getattr(client, 'email3', None)
        return ""
    
    def get_account_manager_name(self, obj):
        if obj.manager_id:
            try:
                manager = Usuario.objects.get(id=obj.manager_id)
                return manager.nombre
            except Usuario.DoesNotExist:
                return ""
        return ""
    
    def get_sales_agent_name(self, obj):
        if obj.agent_id:
            try:
                agent = Usuario.objects.get(id=obj.agent_id)
                return agent.nombre
            except Usuario.DoesNotExist:
                return ""
        return ""
    
    def get_assigned_user_name(self, obj):
        if hasattr(obj, 'user') and obj.user:
            return obj.user.nombre if hasattr(obj.user, 'nombre') else obj.user.username
        elif hasattr(obj, 'user_id') and obj.user_id:
            try:
                user = Usuario.objects.get(id=obj.user_id)
                return user.nombre
            except Usuario.DoesNotExist:
                return ""
        return ""
    
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
