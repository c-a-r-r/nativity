from django.core.management.base import BaseCommand
from trip_registration.models import Country, Pilgrimage
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Create sample countries
        countries = [
            {"id": 1, "name": "United States", "code": "US"},
            {"id": 2, "name": "Canada", "code": "CA"},
            {"id": 3, "name": "United Kingdom", "code": "UK"},
            {"id": 4, "name": "Australia", "code": "AU"},
            {"id": 5, "name": "Germany", "code": "DE"},
        ]
        
        for country_data in countries:
            country, created = Country.objects.get_or_create(
                id=country_data["id"],
                defaults={
                    "name": country_data["name"],
                    "code": country_data["code"]
                }
            )
            if created:
                self.stdout.write(f"Created country: {country.name}")
        
        # Create sample pilgrimage
        pilgrimage_data = {
            "id": 1,
            "title": "Holy Land Pilgrimage 2024",
            "description": "Experience the footsteps of Jesus in the Holy Land",
            "start_date": datetime.now() + timedelta(days=90),
            "end_date": datetime.now() + timedelta(days=100),
            "price": 3299.00,
            "available_spots": 40,
            "status": "active"
        }
        
        pilgrimage, created = Pilgrimage.objects.get_or_create(
            id=pilgrimage_data["id"],
            defaults=pilgrimage_data
        )
        
        if created:
            self.stdout.write(f"Created pilgrimage: {pilgrimage.title}")
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
