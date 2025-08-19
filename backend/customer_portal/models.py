from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomerUser(AbstractUser):
    """
    Customer user model for pilgrimage bookings
    Extends Django's AbstractUser with customer-specific fields
    """
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Address Information
    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, default='United States')
    
    # Church/Organization Information
    church_name = models.CharField(max_length=100, blank=True)
    church_address = models.TextField(blank=True)
    spiritual_director = models.CharField(max_length=100, blank=True)
    
    # Account Settings
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    password_reset_token = models.CharField(max_length=100, blank=True)
    password_reset_expires = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    marketing_emails = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=10, default='en')
    
    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Add related_name to avoid conflicts with users.Usuario
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customer_users',
        related_query_name='customer_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customer_users',
        related_query_name='customer_user',
    )
    
    # Use email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'customer_users'
        verbose_name = 'Customer User'
        verbose_name_plural = 'Customer Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_active_bookings(self):
        """Get all active bookings for this customer"""
        return self.customerbooking_set.filter(
            booking_status__in=['confirmed', 'pending_payment', 'partial_payment']
        )
    
    def get_completed_trips(self):
        """Get all completed trips for this customer"""
        return self.customerbooking_set.filter(booking_status='completed')


class CustomerProfile(models.Model):
    """
    Extended profile information for customers
    Separate from CustomerUser for optional/additional data
    """
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name='profile')
    
    # Emergency Contact Information
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_email = models.EmailField(blank=True)
    
    # Travel Preferences
    dietary_restrictions = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    mobility_requirements = models.TextField(blank=True)
    room_preferences = models.CharField(max_length=20, choices=[
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('twin', 'Twin Beds'),
        ('no_preference', 'No Preference')
    ], default='no_preference')
    
    # Travel Documents
    passport_number = models.CharField(max_length=20, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    passport_country = models.CharField(max_length=50, blank=True)
    
    # Communication Preferences
    preferred_contact_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('sms', 'SMS'),
        ('mail', 'Postal Mail')
    ], default='email')
    
    # Profile Settings
    profile_picture = models.ImageField(upload_to='customer_profiles/', blank=True)
    bio = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customer_profiles'
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'
    
    def __str__(self):
        return f"Profile for {self.user.full_name}"


class EmailVerificationToken(models.Model):
    """
    Email verification tokens for customer registration
    """
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'email_verification_tokens'
        verbose_name = 'Email Verification Token'
        verbose_name_plural = 'Email Verification Tokens'
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Verification token for {self.user.email}"


class PasswordResetToken(models.Model):
    """
    Password reset tokens for customer password recovery
    """
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'password_reset_tokens'
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Password reset token for {self.user.email}"
