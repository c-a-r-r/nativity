from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomerUser, CustomerProfile


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for customer registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomerUser
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'phone', 'church_name', 'spiritual_director',
            'marketing_emails', 'sms_notifications'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirm from validated_data
        validated_data.pop('password_confirm')
        
        # Extract password
        password = validated_data.pop('password')
        
        # Create user
        user = CustomerUser.objects.create_user(
            username=validated_data['email'],  # Use email as username
            password=password,
            **validated_data
        )
        
        # Create profile
        CustomerProfile.objects.create(user=user)
        
        return user


class CustomerLoginSerializer(serializers.Serializer):
    """
    Serializer for customer login
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Custom authentication for CustomerUser
            try:
                from django.contrib.auth.hashers import check_password
                user = CustomerUser.objects.get(email=email)
                if check_password(password, user.password):
                    if not user.is_active:
                        raise serializers.ValidationError('User account is disabled')
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('Invalid email or password')
            except CustomerUser.DoesNotExist:
                raise serializers.ValidationError('Invalid email or password')
        else:
            raise serializers.ValidationError('Must include email and password')


class CustomerUserSerializer(serializers.ModelSerializer):
    """
    Serializer for customer user information
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomerUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'date_of_birth', 'address_line1', 'address_line2',
            'city', 'state', 'zip_code', 'country', 'church_name',
            'church_address', 'spiritual_director', 'marketing_emails',
            'sms_notifications', 'preferred_language', 'date_joined',
            'last_login', 'is_email_verified'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_email_verified']


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer profile information
    """
    user = CustomerUserSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = [
            'user', 'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'emergency_contact_email',
            'dietary_restrictions', 'medical_conditions', 'mobility_requirements',
            'room_preferences', 'passport_number', 'passport_expiry',
            'passport_country', 'preferred_contact_method', 'profile_picture',
            'bio', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    current_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = CustomerUser.objects.get(email=value)
        except CustomerUser.DoesNotExist:
            raise serializers.ValidationError('No account found with this email address')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation
    """
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
