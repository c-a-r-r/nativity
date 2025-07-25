# Generated by Django 4.2.23 on 2025-07-14 02:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_id', models.IntegerField(db_index=True)),
                ('trip_name', models.CharField(max_length=255)),
                ('church_name', models.CharField(blank=True, max_length=255)),
                ('spiritual_director', models.CharField(blank=True, max_length=255)),
                ('departure_date', models.DateField()),
                ('arrival_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('custom_title', models.CharField(blank=True, max_length=255)),
                ('custom_description', models.TextField(blank=True)),
                ('custom_itinerary', models.JSONField(blank=True, default=dict)),
                ('includes', models.JSONField(blank=True, default=list)),
                ('excludes', models.JSONField(blank=True, default=list)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('is_published', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TripTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('duration_days', models.IntegerField()),
                ('trip_title', models.CharField(max_length=255)),
                ('trip_description', models.TextField()),
                ('hero_image', models.URLField(blank=True)),
                ('gallery_images', models.JSONField(blank=True, default=list)),
                ('daily_itinerary', models.JSONField(blank=True, default=dict)),
                ('video_url', models.URLField(blank=True)),
                ('brochure_url', models.URLField(blank=True)),
                ('default_includes', models.JSONField(blank=True, default=list)),
                ('default_excludes', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TripRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=50)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=100)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=20)),
                ('dietary_restrictions', models.TextField(blank=True)),
                ('medical_conditions', models.TextField(blank=True)),
                ('special_requests', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='marketing.trip')),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing.triptemplate'),
        ),
        migrations.CreateModel(
            name='PrivateAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('contact_id', models.IntegerField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_tokens', to='marketing.trip')),
            ],
        ),
    ]
