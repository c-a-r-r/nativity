from django.db import models
from django.utils.text import slugify
import uuid


# --- Template Destination Model ---
class TemplateDestination(models.Model):
    """Destination options for marketing trip templates"""
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# --- Marketing Trip Template Model ---
class MarketingTripTemplate(models.Model):
    """Reusable marketing trip templates for dynamic trip site generation"""
    name = models.CharField(max_length=255)
    trip_title = models.CharField(max_length=255)
    promo_text = models.TextField(blank=True)
    hero_image = models.URLField(blank=True)
    video_link = models.URLField(blank=True)
    brochure_link = models.URLField(blank=True)
    itinerary = models.JSONField(default=list, blank=True)
    gallery = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    destination = models.ForeignKey(TemplateDestination, on_delete=models.SET_NULL, null=True, blank=True, related_name='templates')
    slug = models.SlugField(unique=True, max_length=128, default=uuid.uuid4)

    def __str__(self):
        return f"{self.name} - {self.trip_title}"

# --- Marketing Trip Model ---
class MarketingTrip(models.Model):
    """Generated marketing trip instance for public/private pages"""
    id = models.AutoField(primary_key=True)
    quote = models.ForeignKey('quotes.Quote', on_delete=models.CASCADE, related_name='trips')
    template = models.ForeignKey(MarketingTripTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_trips')
    trip_title = models.CharField(max_length=255)
    promo_text = models.TextField(blank=True)
    hero_image = models.URLField(blank=True)
    itinerary = models.JSONField(default=list, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    departure_city = models.CharField(max_length=255, blank=True)
    trip_includes = models.TextField(blank=True, null=True)
    trip_not_includes = models.TextField(blank=True, null=True)
    spiritual_director = models.CharField(max_length=255, blank=True)
    brochure = models.URLField(blank=True)
    video_link = models.URLField(blank=True)
    contact_info = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=128, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"Trip: {self.trip_title} ({self.slug})"