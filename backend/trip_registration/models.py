"""
Trip Registration Models
Mirrors the exact MySQL table structure from the existing PHP system
"""
from django.db import models


class Client(models.Model):
    """
    Main client table - mirrors existing MySQL client table exactly
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    passport = models.CharField(max_length=50, null=True, blank=True)
    passport_exp = models.DateField(null=True, blank=True)
    passport_country = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, null=True, blank=True)
    shirt_size = models.CharField(max_length=10, null=True, blank=True)
    dietary_restrictions = models.TextField(null=True, blank=True)
    medical_conditions = models.TextField(null=True, blank=True)
    know_us = models.CharField(max_length=500, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    birthday_formatted = models.CharField(max_length=20, null=True, blank=True)
    passport_exp_formatted = models.CharField(max_length=20, null=True, blank=True)
    # Image fields
    passport_img_front = models.CharField(max_length=255, null=True, blank=True)
    passport_img_back = models.CharField(max_length=255, null=True, blank=True)
    drivers_license_front = models.CharField(max_length=255, null=True, blank=True)
    drivers_license_back = models.CharField(max_length=255, null=True, blank=True)
    selfie_passport = models.CharField(max_length=255, null=True, blank=True)
    # Additional fields
    special_assistance = models.TextField(null=True, blank=True)
    room_preference = models.CharField(max_length=100, null=True, blank=True)
    roommate_preference = models.CharField(max_length=100, null=True, blank=True)
    previous_traveler = models.CharField(max_length=10, null=True, blank=True)
    preferred_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=20, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    mobile_phone = models.CharField(max_length=50, null=True, blank=True)
    work_phone = models.CharField(max_length=50, null=True, blank=True)
    business_email = models.CharField(max_length=150, null=True, blank=True)
    personal_email = models.CharField(max_length=150, null=True, blank=True)
    social_security = models.CharField(max_length=20, null=True, blank=True)
    employer = models.CharField(max_length=200, null=True, blank=True)
    business_address = models.CharField(max_length=200, null=True, blank=True)
    business_city = models.CharField(max_length=100, null=True, blank=True)
    business_state = models.CharField(max_length=100, null=True, blank=True)
    business_zip = models.CharField(max_length=20, null=True, blank=True)
    business_country = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        managed = False  # Don't manage this table - it exists in the DB
        db_table = 'client'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    
    def __str__(self):
        return f"{self.name} {self.lastname}"


class ClientTmp(models.Model):
    """
    Temporary client table - mirrors existing MySQL client_tmp table exactly
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    passport = models.CharField(max_length=50, null=True, blank=True)
    passport_exp = models.DateField(null=True, blank=True)
    passport_country = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, null=True, blank=True)
    shirt_size = models.CharField(max_length=10, null=True, blank=True)
    dietary_restrictions = models.TextField(null=True, blank=True)
    medical_conditions = models.TextField(null=True, blank=True)
    know_us = models.CharField(max_length=500, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    birthday_formatted = models.CharField(max_length=20, null=True, blank=True)
    passport_exp_formatted = models.CharField(max_length=20, null=True, blank=True)
    # Additional fields specific to tmp table
    session_id = models.CharField(max_length=100, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    payment_attempted = models.BooleanField(default=False)
    
    class Meta:
        managed = False  # Don't manage this table - it exists in the DB
        db_table = 'client_tmp'
        verbose_name = 'Temporary Client'
        verbose_name_plural = 'Temporary Clients'
    
    def __str__(self):
        return f"Temp: {self.name} {self.lastname}"


class PilgrimageClient(models.Model):
    """
    Pilgrimage client registration - mirrors existing MySQL pilgrimage_client table exactly
    """
    id = models.AutoField(primary_key=True)
    pilgrimage_id = models.IntegerField()
    client_id = models.IntegerField()
    ap = models.CharField(max_length=50, null=True, blank=True)
    gsv = models.CharField(max_length=10, null=True, blank=True)
    departurecity_id = models.IntegerField(null=True, blank=True)
    landonly = models.CharField(max_length=10, null=True, blank=True)
    totalcost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.CharField(max_length=50, null=True, blank=True)
    paymentoption = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.TextField(null=True, blank=True)
    lastname = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    fax = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    zipcode = models.TextField(null=True, blank=True)
    birthday = models.TextField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True)
    occupation = models.TextField(null=True, blank=True)
    passport = models.TextField(null=True, blank=True)
    passport_exp = models.TextField(null=True, blank=True)
    passport_country = models.TextField(null=True, blank=True)
    nationality = models.TextField(null=True, blank=True)
    emergency_contact = models.TextField(null=True, blank=True)
    emergency_contact_phone = models.TextField(null=True, blank=True)
    shirt_size = models.TextField(null=True, blank=True)
    dietary_restrictions = models.TextField(null=True, blank=True)
    medical_conditions = models.TextField(null=True, blank=True)
    know_us = models.TextField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    room_preference = models.TextField(null=True, blank=True)
    roommate_preference = models.TextField(null=True, blank=True)
    previous_traveler = models.TextField(null=True, blank=True)
    preferred_name = models.TextField(null=True, blank=True)
    middle_name = models.TextField(null=True, blank=True)
    suffix = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    address2 = models.TextField(null=True, blank=True)
    mobile_phone = models.TextField(null=True, blank=True)
    work_phone = models.TextField(null=True, blank=True)
    business_email = models.TextField(null=True, blank=True)
    personal_email = models.TextField(null=True, blank=True)
    social_security = models.TextField(null=True, blank=True)
    employer = models.TextField(null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)
    business_city = models.TextField(null=True, blank=True)
    business_state = models.TextField(null=True, blank=True)
    business_zip = models.TextField(null=True, blank=True)
    business_country = models.TextField(null=True, blank=True)
    special_assistance = models.TextField(null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False  # Don't manage this table - it exists in the DB
        db_table = 'pilgrimage_client'
        verbose_name = 'Pilgrimage Client'
        verbose_name_plural = 'Pilgrimage Clients'
    
    def __str__(self):
        return f"Pilgrimage {self.pilgrimage_id} - Client {self.client_id}"


class PilgrimageClientTmp(models.Model):
    """
    Temporary pilgrimage client registration - mirrors existing MySQL pilgrimage_client_tmp table exactly
    """
    id = models.AutoField(primary_key=True)
    pilgrimage_id = models.IntegerField()
    client_id = models.IntegerField(null=True, blank=True)
    ap = models.CharField(max_length=50, null=True, blank=True)
    gsv = models.CharField(max_length=10, null=True, blank=True)
    departurecity_id = models.IntegerField(null=True, blank=True)
    landonly = models.CharField(max_length=10, null=True, blank=True)
    totalcost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.CharField(max_length=50, null=True, blank=True)
    paymentoption = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.TextField(null=True, blank=True)
    lastname = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    fax = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    zipcode = models.TextField(null=True, blank=True)
    birthday = models.TextField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True)
    occupation = models.TextField(null=True, blank=True)
    passport = models.TextField(null=True, blank=True)
    passport_exp = models.TextField(null=True, blank=True)
    passport_country = models.TextField(null=True, blank=True)
    nationality = models.TextField(null=True, blank=True)
    emergency_contact = models.TextField(null=True, blank=True)
    emergency_contact_phone = models.TextField(null=True, blank=True)
    shirt_size = models.TextField(null=True, blank=True)
    dietary_restrictions = models.TextField(null=True, blank=True)
    medical_conditions = models.TextField(null=True, blank=True)
    know_us = models.TextField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    room_preference = models.TextField(null=True, blank=True)
    roommate_preference = models.TextField(null=True, blank=True)
    previous_traveler = models.TextField(null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # Temporary table specific fields
    session_id = models.CharField(max_length=100, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    payment_attempted = models.BooleanField(default=False)
    authorize_net_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_response = models.TextField(null=True, blank=True)
    
    class Meta:
        managed = False  # Don't manage this table - it exists in the DB
        db_table = 'pilgrimage_client_tmp'
        verbose_name = 'Temporary Pilgrimage Client'
        verbose_name_plural = 'Temporary Pilgrimage Clients'
    
    def __str__(self):
        return f"Temp Pilgrimage {self.pilgrimage_id} - Client {self.client_id}"


class Country(models.Model):
    """
    Country lookup table - mirrors existing MySQL country table exactly
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=2, null=True, blank=True)
    
    class Meta:
        managed = False  # Don't manage this table - it exists in the DB
        db_table = 'country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        return self.nombre


class Pilgrimage(models.Model):
    """
    Pilgrimage table - mirrors existing MySQL pilgrimage table exactly
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    departure_date = models.DateField()
    return_date = models.DateField()
    registration_deadline = models.DateField()
    max_participants = models.IntegerField(default=0)
    current_participants = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='active')
    slug = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False  # Don't manage this table - it exists in the DB
        db_table = 'pilgrimage'
        verbose_name = 'Pilgrimage'
        verbose_name_plural = 'Pilgrimages'
    
    def __str__(self):
        return self.name
