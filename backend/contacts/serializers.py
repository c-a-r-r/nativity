from django.utils import timezone          # ← new
from rest_framework import serializers
from .models import Client, YN_CHOICES
import datetime

class NullableIntegerField(serializers.IntegerField):
    """
    Custom IntegerField that turns an empty string ("") into None
    before the usual integer validation occurs.
    """
    def to_internal_value(self, data):
        if data in ("", None):        # allow POST/PUT/PATCH sending "" or null
            return None
        return super().to_internal_value(data)

class ClientSerializer(serializers.ModelSerializer):
    client_type_display = serializers.CharField(source='client_type.nombre', read_only=True)
    date_birth = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d', ''])
    pp_date_issue = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d', ''])
    pp_date_expire = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d', ''])
    # ...other fields...

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('date_created', 'date_updated')
        extra_kwargs = {
            'date_birth': {'required': False, 'allow_null': True},
            'pp_date_issue': {'required': False, 'allow_null': True},
            'pp_date_expire': {'required': False, 'allow_null': True},
        }

    # keep this indented inside the class ↓
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.date_updated = timezone.now()  # bump timestamp
        instance.save()
        return instance
    # Prevent date fields from being set to '1900-01-01'
    def validate_date_birth(self, value):
        if value == datetime.date(1900, 1, 1):
            return None
        return value

    def validate_pp_date_issue(self, value):
        if value == datetime.date(1900, 1, 1):
            return None
        return value

    def validate_pp_date_expire(self, value):
        if value == datetime.date(1900, 1, 1):
            return None
        return value