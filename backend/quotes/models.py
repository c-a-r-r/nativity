from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class QuoteStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=155, db_column="nombre")

    class Meta:
        db_table = "quote_status"
        managed = False

    def __str__(self):
        return self.nombre
    
class ItineraryCity(models.Model):  # <-- Rename class
    city_code = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=125, blank=True, null=True)
    cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'itinerary_cities'
        managed = False

    def __str__(self):
        return f"{self.city_code} - {self.city} + (${self.cost})"

    def short_display(self):
        return f"{self.city_code} - {self.city}"
    
class QuoteWorkflow(models.Model):
    nombre = models.CharField(max_length=255, db_column='nombre')

    class Meta:
        db_table = 'quote_workflow'
        managed = False

    def __str__(self):
        return self.nombre
    
class Client(models.Model):
    client_type = models.ForeignKey('ClientType', on_delete=models.SET_NULL, null=True, blank=True)  # Assuming a ClientType model exists
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,   # or whatever is appropriate
        related_name='clients'
    )
    date_created = models.DateField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=155, default='', blank=True)
    last_name = models.CharField(max_length=155, default='', blank=True)
    middle_name = models.CharField(max_length=155, default='', blank=True)
    company = models.CharField(max_length=155, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=35, null=True, blank=True)
    zip = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)
    phone2 = models.CharField(max_length=45, null=True, blank=True)
    phone3 = models.CharField(max_length=45, null=True, blank=True)
    mobile = models.CharField(max_length=45, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    email2 = models.EmailField(max_length=255, null=True, blank=True)
    email3 = models.EmailField(max_length=255, null=True, blank=True)
    email_maillist = models.CharField(max_length=1, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]  
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, null=True, blank=True)
    date_birth = models.DateField(null=True, blank=True)
    ems_name = models.CharField(max_length=150, null=True, blank=True)
    ems_phone = models.CharField(max_length=50, null=True, blank=True)
    pp_number = models.CharField(max_length=50, null=True, blank=True)
    pp_date_issue = models.DateField(null=True, blank=True)
    pp_date_expire = models.DateField(null=True, blank=True)
    pp_place_issue = models.CharField(max_length=150, null=True, blank=True)
    pp_nationality = models.CharField(max_length=200, null=True, blank=True)
    want_single_room = models.CharField(max_length=1, null=True, blank=True)
    want_roomate = models.CharField(max_length=1, null=True, blank=True)
    have_roomate = models.CharField(max_length=1, null=True, blank=True)
    have_roomate_name = models.CharField(max_length=150, null=True, blank=True)
    have_roomate_id = models.PositiveIntegerField(null=True, blank=True)
    registered_at_event = models.CharField(max_length=1, null=True, blank=True)
    #archdiocese = models.ForeignKey('ClientGroup', on_delete=models.SET_NULL, blank=True, null=True)
    mail_lists = models.CharField(max_length=255, null=True, blank=True)
    name_tag = models.CharField(max_length=255, null=True, blank=True)
    from_web = models.CharField(max_length=1, default='N', blank=True)
    hearabout = models.CharField(max_length=255, null=True, blank=True)
    unique_ident = models.CharField(max_length=35, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        managed = False
        db_table = 'client'


class Quote(models.Model):
    group_name = models.CharField(max_length=255, blank=True, null=True)
    church_name = models.CharField(max_length=255, blank=True, null=True)
    leader_name = models.CharField(max_length=255, blank=True, null=True)
    client = models.ForeignKey(
    Client,
    on_delete=models.SET_NULL,
    null=True,
    db_column="client_id",
    db_constraint=False)
    coordinator_name = models.CharField(max_length=255, blank=True, null=True)
    coordinator_phone = models.CharField(max_length=55, blank=True, null=True)
    coordinator_email = models.CharField(max_length=255, blank=True, null=True)
    sugested_date = models.CharField(max_length=255, blank=True, null=True)
    leader_free = models.CharField(max_length=1, blank=True, null=True)
    free_each = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    itinerary_id = models.IntegerField(blank=True, null=True)
    trip_name = models.CharField(max_length=255, blank=True, null=True)
    itinerary_cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    #departure_city_id = models.IntegerField(blank=True, null=True)
    departure_city_id = models.ForeignKey(
        ItineraryCity,
        on_delete=models.SET_NULL,
        null=True,
        db_column='departure_city_id')
    departure_city_cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    additional_cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    comision_usuario = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    comision_leader = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    display_commission_fundraiser = models.CharField(max_length=3)
    departure_date = models.DateField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    quote_status = models.ForeignKey(
        QuoteStatus,
        on_delete=models.SET_NULL,
        null=True,
        db_column="quote_status_id"
    )
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    utilization_date = models.DateField(blank=True, null=True)
    full_payment_date = models.DateField(blank=True, null=True)
    txt_air = models.TextField(blank=True, null=True)
    txt_hotel = models.TextField(blank=True, null=True)
    txt_land = models.TextField(blank=True, null=True)
    txt_mass = models.TextField(blank=True, null=True)
    manager_id = models.IntegerField(blank=True, null=True)
    agent_id = models.IntegerField(blank=True, null=True)
    air = models.CharField(max_length=255, blank=True, null=True)
    land = models.CharField(max_length=255, blank=True, null=True)
    add_notes = models.CharField(max_length=255, blank=True, null=True)
    mail1 = models.DateField(blank=True, null=True)
    mail2 = models.DateField(blank=True, null=True)
    mail3 = models.DateField(blank=True, null=True)
    mail4 = models.DateField(blank=True, null=True)
    mail5 = models.DateField(blank=True, null=True)
    mail6 = models.DateField(blank=True, null=True)
    mail_sent1 = models.DateField(blank=True, null=True)
    mail_sent2 = models.DateField(blank=True, null=True)
    mail_sent3 = models.DateField(blank=True, null=True)
    mail_sent4 = models.DateField(blank=True, null=True)
    mail_sent5 = models.DateField(blank=True, null=True)
    mail_sent6 = models.DateField(blank=True, null=True)
    mail_weekly = models.CharField(max_length=1, blank=True, null=True)
    mail_weekly1 = models.CharField(max_length=255, blank=True, null=True)
    mail_weekly2 = models.CharField(max_length=255, blank=True, null=True)
    mail_weekly3 = models.CharField(max_length=255, blank=True, null=True)
    mail_weekly_sent = models.DateField(blank=True, null=True)
    custom = models.IntegerField(blank=True, null=True)
    is_dmc = models.IntegerField()
    lunch_included = models.CharField(max_length=3, blank=True, null=True)
    tip_included = models.CharField(max_length=3, blank=True, null=True)
    lunch_and_tip_includes = models.IntegerField(blank=True, null=True, db_comment='0 - Does NOT Include Lunch and Tips, 1 - Includes Lunch, 2 - Includes Tips, 3 - Includes Lunch and Tips')
    cancelation_terms = models.CharField(max_length=45, blank=True, null=True)
    pax15 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    pax20 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    pax25 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    pax30 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    pax35 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    pax40 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    pax45 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    pax50 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    custom_itenirary = models.TextField(blank=True, null=True)
    cost_marketing = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    cost_bus = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    cost_air = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    cost_land = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    cost_misc = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    cost_total = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    request = models.TextField(blank=True, null=True)
    ems_contacts = models.TextField(blank=True, null=True)
    workflow_status_rel = models.ForeignKey(
        QuoteWorkflow, # The model this Quote is related to (the workflow status)
        on_delete=models.SET_NULL, # What happens when the related QuoteWorkflow is deleted
        null=True, # Allow the field to be NULL in the database
        blank=True, # Allow the field to be blank in forms/admin
        db_column='workflow_status' # Crucial: Maps to the existing 'workflow_status' database column
    )
    mkt_file1 = models.CharField(max_length=250, blank=True, null=True)
    mkt_file2 = models.CharField(max_length=250, blank=True, null=True)
    mkt_file3 = models.CharField(max_length=250, blank=True, null=True)
    mkt_file4 = models.CharField(max_length=250, blank=True, null=True)
    mkt_link1 = models.CharField(max_length=250, blank=True, null=True)
    mkt_link2 = models.CharField(max_length=250, blank=True, null=True)
    mkt_link3 = models.CharField(max_length=250, blank=True, null=True)
    fecha_confirmado = models.DateField(blank=True, null=True)
    publish_website = models.CharField(max_length=3, blank=True, null=True)
    single_room_price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    mkt_location = models.CharField(max_length=250, blank=True, null=True)
    mkt_shiped = models.CharField(max_length=3)
    mkt_tracking_no = models.CharField(max_length=255, blank=True, null=True)
    mkt_progress = models.CharField(max_length=75, blank=True, null=True)
    lunch_cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    tips_cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_deposit = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    custom_aproved = models.CharField(max_length=75, blank=True, null=True)
    free_each_cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    charge_city_fee = models.CharField(max_length=3, blank=True, null=True)
    mkt_website_id = models.IntegerField(blank=True, null=True)
    trip_includes = models.TextField(blank=True, null=True)
    trip_not_include = models.TextField(blank=True, null=True)
    total_cost_land_only = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    multi_city = models.CharField(max_length=1, blank=True, null=True)
    multi_city_same_fee = models.TextField(blank=True, null=True)
    dep_city_id1 = models.IntegerField(blank=True, null=True)
    dep_city_id2 = models.IntegerField(blank=True, null=True)
    dep_city_id3 = models.IntegerField(blank=True, null=True)
    dep_city_id4 = models.IntegerField(blank=True, null=True)
    dep_city_id5 = models.IntegerField(blank=True, null=True)
    dep_city_id6 = models.IntegerField(blank=True, null=True)
    dep_city_id7 = models.IntegerField(blank=True, null=True)
    dep_city_id8 = models.IntegerField(blank=True, null=True)
    dep_city_id9 = models.IntegerField(blank=True, null=True)
    dep_city_cost1 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    dep_city_cost2 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    dep_city_cost3 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    dep_city_cost4 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    dep_city_cost5 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    dep_city_cost6 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    dep_city_cost7 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    dep_city_cost8 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    dep_city_cost9 = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    terms_template_id = models.IntegerField(blank=True, null=True)
    final_itenirary = models.TextField(blank=True, null=True)

    # --- Marketing Trip Links ---
    marketing_public_link = models.CharField(max_length=512, blank=True, null=True)
    marketing_private_link = models.CharField(max_length=512, blank=True, null=True)
    max_pax = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'quote'

    def __str__(self):
        return f"Quote {self.id} - {self.group_name or 'No Group Name'}"
    
    def get_full_name(self):
        return self.nombre
    
    # Add the new methods here:
    def create_trip_from_template(self, template_id):
        """Create a marketing trip using a template and quote data"""
        from marketing.models import Trip, TripTemplate, PrivateAccessToken
        
        template = TripTemplate.objects.get(id=template_id)
        
        # Extract church name and spiritual director from quote fields
        church_name = self.church_name or (self.client.company if self.client else '')
        spiritual_director = self.leader_name or (self.client.first_name + ' ' + self.client.last_name if self.client else '')
        
        trip = Trip.objects.create(
            quote_id=self.id,  # Use quote_id instead of quote
            template=template,
            trip_name=f"{template.name} - {church_name}",
            church_name=church_name,
            spiritual_director=spiritual_director,
            departure_date=self.departure_date,
            arrival_date=self.arrival_date,
            price=self.total_cost,
            
            includes=self.get_includes_list(),
            excludes=self.get_excludes_list(),
            
            is_published=False
        )
        
        # Create private access token for the main contact
        if self.client:
            PrivateAccessToken.objects.create(
                trip=trip,
                contact_id=self.client.id  # Use contact_id instead of contact
            )
        
        return trip

    def get_includes_list(self):
        """Extract what's included from quote fields"""
        includes = []
        
        # Based on your quote model, extract includes from text fields
        if self.trip_includes:
            # Split by newlines or other delimiter
            includes = [item.strip() for item in self.trip_includes.split('\n') if item.strip()]
        
        # Add other standard includes based on quote settings
        if self.lunch_included == 'Yes':
            includes.append('Daily breakfast and lunch')
        
        if self.tip_included == 'Yes':
            includes.append('Tips for guides and drivers')
            
        # Add air/land info if available
        if self.air:
            includes.append(f'Air transportation: {self.air}')
            
        if self.land:
            includes.append(f'Land transportation: {self.land}')
            
        return includes

    def get_excludes_list(self):
        """Extract what's not included"""
        excludes = []
        
        # Based on your quote model
        if self.trip_not_include:
            excludes = [item.strip() for item in self.trip_not_include.split('\n') if item.strip()]
        
        # Add standard excludes based on quote settings
        if self.lunch_included != 'Yes':
            excludes.append('Lunch meals (unless specified)')
            
        if self.tip_included != 'Yes':
            excludes.append('Tips for guides and drivers')
            
        # Standard excludes
        excludes.extend([
            'Personal expenses',
            'Travel insurance (recommended)',
            'Items not mentioned in the itinerary'
        ])
        
        return excludes

    @property
    def total_due(self):
        """Get the total amount due for this quote"""
        return self.total_cost or 0
    
class ClientGroup(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
    
    
class ClientType(models.Model):
    name = models.CharField(max_length=155, unique=True)

    class Meta:
        db_table = 'client_type'
        managed = False
        
    def __str__(self):
        return self.name
    
class MktProgressStatus(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Mkt Progress Statuses"
        managed = False

class DestinationGroup(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'destination_group'
        verbose_name = 'Destination Group'
        verbose_name_plural = 'Destination Groups'
        managed = False

    def __str__(self):
        return self.nombre or f"Group {self.id}"
    
class Destination(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    nombre_spa = models.CharField(max_length=255, null=True, blank=True)
    template = models.TextField(null=True, blank=True)
    template_spa = models.TextField(null=True, blank=True)
    it_template = models.TextField(null=True, blank=True)
    it_template_spa = models.TextField(null=True, blank=True)
    trip_days = models.IntegerField()
    prep_guide1 = models.IntegerField(null=True, blank=True)
    prep_guide2 = models.IntegerField(null=True, blank=True)
    prep_guide3 = models.IntegerField(null=True, blank=True)
    prep_guide4 = models.IntegerField(null=True, blank=True)
    reminder_sheet1 = models.IntegerField(null=True, blank=True)
    reminder_sheet2 = models.IntegerField(null=True, blank=True)
    reminder_sheet3 = models.IntegerField(null=True, blank=True)
    reminder_sheet4 = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'destination'
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'
        managed = False

    def __str__(self):
        return self.nombre or f"Destination {self.id}"