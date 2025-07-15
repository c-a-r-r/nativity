from django.db import models
from django.utils.text import slugify
import uuid

class TripTemplate(models.Model):
    """Reusable templates for different destinations and trip types"""
    name = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    duration_days = models.IntegerField()
    
    # Template content
    trip_title = models.CharField(max_length=255)
    trip_description = models.TextField()
    
    # Gallery images (template defaults)
    hero_image = models.URLField(blank=True)
    gallery_images = models.JSONField(default=list, blank=True)
    
    # Daily itinerary template
    daily_itinerary = models.JSONField(default=dict, blank=True)
    
    # Video and brochure
    video_url = models.URLField(blank=True)
    brochure_url = models.URLField(blank=True)
    
    # Default includes/excludes
    default_includes = models.JSONField(default=list, blank=True)
    default_excludes = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.duration_days} days)"

class Trip(models.Model):
    # Fixed: Remove the foreign key constraint and use integer field instead
    # Since Quote model is managed=False, we'll use a simple integer field
    quote_id = models.IntegerField(db_index=True)
    template = models.ForeignKey(TripTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Auto-populated from quote
    trip_name = models.CharField(max_length=255)
    church_name = models.CharField(max_length=255, blank=True)
    spiritual_director = models.CharField(max_length=255, blank=True)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Override template content if needed
    custom_title = models.CharField(max_length=255, blank=True)
    custom_description = models.TextField(blank=True)
    custom_itinerary = models.JSONField(default=dict, blank=True)
    
    # Trip includes/excludes
    includes = models.JSONField(default=list, blank=True)
    excludes = models.JSONField(default=list, blank=True)
    
    # Generated URLs
    slug = models.SlugField(max_length=255, unique=True) 
    
    # Marketing settings
    is_published = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.trip_name}-{self.church_name}")
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    @property
    def quote(self):
        """Get the related quote object"""
        from quotes.models import Quote
        try:
            return Quote.objects.get(id=self.quote_id)
        except Quote.DoesNotExist:
            return None
    
    @property
    def final_title(self):
        return self.custom_title or (self.template.trip_title if self.template else self.trip_name)
    
    @property
    def final_description(self):
        return self.custom_description or (self.template.trip_description if self.template else "")
    
    @property
    def final_itinerary(self):
        return self.custom_itinerary or (self.template.daily_itinerary if self.template else {})
    
    @property
    def final_includes(self):
        return self.includes or (self.template.default_includes if self.template else [])
    
    @property
    def final_excludes(self):
        return self.excludes or (self.template.default_excludes if self.template else [])

class PrivateAccessToken(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='private_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    # Fixed: Use the correct Client model reference
    contact_id = models.IntegerField(db_index=True)  # Use integer field instead of FK
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    @property
    def contact(self):
        """Get the related contact object"""
        from contacts.models import Client
        try:
            return Client.objects.get(id=self.contact_id)
        except Client.DoesNotExist:
            return None
    
    def __str__(self):
        contact = self.contact
        if contact:
            return f"Private access for {contact.first_name} - {self.trip.trip_name}"
        return f"Private access for Contact {self.contact_id} - {self.trip.trip_name}"

class TripRegistration(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='registrations')
    
    # Passenger details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Additional passenger info
    date_of_birth = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Special requirements
    dietary_restrictions = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    special_requests = models.TextField(blank=True)
    
    # Registration status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)

# Aliases for backward compatibility
WebsiteTemplate = TripTemplate
TripInstance = Trip