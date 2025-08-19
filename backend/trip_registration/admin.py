"""
Trip Registration Admin Interface
Django admin configuration for managing registrations
"""
from django.contrib import admin
from .models import (
    Client, ClientTmp, PilgrimageClient, PilgrimageClientTmp, 
    Country, Pilgrimage
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastname', 'email', 'phone', 'country', 'add_date']
    list_filter = ['country', 'gender', 'add_date']
    search_fields = ['name', 'lastname', 'email', 'phone', 'passport']
    readonly_fields = ['add_date', 'modified']
    ordering = ['-add_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'name', 'lastname', 'preferred_name', 'middle_name', 'suffix')
        }),
        ('Contact Information', {
            'fields': ('email', 'personal_email', 'business_email', 'phone', 'mobile_phone', 'work_phone', 'fax')
        }),
        ('Address Information', {
            'fields': ('address', 'address2', 'city', 'state', 'zipcode', 'country')
        }),
        ('Business Information', {
            'fields': ('employer', 'occupation', 'business_address', 'business_city', 'business_state', 'business_zip', 'business_country'),
            'classes': ('collapse',)
        }),
        ('Personal Details', {
            'fields': ('birthday', 'gender', 'nationality', 'social_security')
        }),
        ('Travel Documents', {
            'fields': ('passport', 'passport_exp', 'passport_country', 'passport_img_front', 'passport_img_back', 'drivers_license_front', 'drivers_license_back', 'selfie_passport')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_contact_phone')
        }),
        ('Preferences & Requirements', {
            'fields': ('shirt_size', 'dietary_restrictions', 'medical_conditions', 'special_assistance', 'room_preference', 'roommate_preference', 'previous_traveler')
        }),
        ('Additional Information', {
            'fields': ('know_us', 'observations'),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('add_date', 'modified', 'birthday_formatted', 'passport_exp_formatted'),
            'classes': ('collapse',)
        })
    )


@admin.register(ClientTmp)
class ClientTmpAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastname', 'email', 'session_id', 'expires_at', 'payment_attempted', 'add_date']
    list_filter = ['payment_attempted', 'expires_at', 'add_date']
    search_fields = ['name', 'lastname', 'email', 'session_id']
    readonly_fields = ['add_date', 'modified']
    ordering = ['-add_date']
    
    def has_add_permission(self, request):
        # Don't allow manual creation of temp records
        return False


@admin.register(PilgrimageClient)
class PilgrimageClientAdmin(admin.ModelAdmin):
    list_display = ['get_client_name', 'pilgrimage_id', 'ap', 'totalcost', 'payed', 'paymentoption', 'add_date']
    list_filter = ['pilgrimage_id', 'paymentoption', 'landonly', 'add_date']
    search_fields = ['client_id', 'ap', 'coupon']
    readonly_fields = ['add_date', 'modified']
    ordering = ['-add_date']
    
    def get_client_name(self, obj):
        if obj.client_id:
            try:
                client = Client.objects.get(id=obj.client_id)
                return f"{client.name} {client.lastname}"
            except Client.DoesNotExist:
                return f"Client ID: {obj.client_id}"
        return "No Client"
    get_client_name.short_description = 'Client Name'
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('pilgrimage_id', 'client_id', 'ap', 'gsv')
        }),
        ('Payment Information', {
            'fields': ('totalcost', 'payed', 'discount', 'coupon', 'paymentoption', 'departurecity_id', 'landonly')
        }),
        ('Passenger Data', {
            'fields': ('firstname', 'lastname', 'email', 'phone'),
            'description': 'These fields contain JSON arrays of passenger data'
        }),
        ('System Fields', {
            'fields': ('add_date', 'modified'),
            'classes': ('collapse',)
        })
    )


@admin.register(PilgrimageClientTmp)
class PilgrimageClientTmpAdmin(admin.ModelAdmin):
    list_display = ['pilgrimage_id', 'session_id', 'expires_at', 'payment_attempted', 'authorize_net_transaction_id', 'add_date']
    list_filter = ['pilgrimage_id', 'payment_attempted', 'expires_at', 'add_date']
    search_fields = ['session_id', 'authorize_net_transaction_id', 'ap']
    readonly_fields = ['add_date', 'modified']
    ordering = ['-add_date']
    
    def has_add_permission(self, request):
        # Don't allow manual creation of temp records
        return False
    
    actions = ['cleanup_expired']
    
    def cleanup_expired(self, request, queryset):
        from django.utils import timezone
        expired = queryset.filter(expires_at__lt=timezone.now())
        count = expired.count()
        expired.delete()
        self.message_user(request, f"Cleaned up {count} expired registrations.")
    cleanup_expired.short_description = "Clean up expired registrations"


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'id']
    search_fields = ['nombre', 'codigo']
    ordering = ['nombre']


@admin.register(Pilgrimage)
class PilgrimageAdmin(admin.ModelAdmin):
    list_display = ['name', 'departure_date', 'return_date', 'cost', 'max_participants', 'current_participants', 'status']
    list_filter = ['status', 'departure_date', 'return_date']
    search_fields = ['name', 'slug', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-departure_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'slug')
        }),
        ('Trip Details', {
            'fields': ('departure_date', 'return_date', 'cost', 'registration_deadline')
        }),
        ('Capacity', {
            'fields': ('max_participants', 'current_participants', 'status')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
