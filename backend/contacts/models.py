from django.conf import settings
from django.db import models

# ----------------------------------------------------------------------------
# Lookup table: ClientType
# ----------------------------------------------------------------------------

class ClientType(models.Model):
    id     = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=155, unique=True)

    class Meta:
        db_table = 'client_type'
        ordering = ['nombre']
        managed  = False  # ← change to True if Django should manage the table
        verbose_name = 'Client Type'
        verbose_name_plural = 'Client Types'

    def __str__(self):
        return self.nombre


# ----------------------------------------------------------------------------
# Main table: Client
# ----------------------------------------------------------------------------
YN_CHOICES = (
    ('N', 'No'),
    ('Y', 'Yes'),
)

class Client(models.Model):
    id = models.AutoField(primary_key=True)

    # ─────────── foreign keys ───────────
    parent_client = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        db_column='parent_client_id', related_name='children'
    )
    booking_id = models.IntegerField(null=True, blank=True)  # adjust to FK if Booking model exists

    client_type = models.ForeignKey(
        ClientType, on_delete=models.PROTECT, null=True, blank=True,
        db_column='client_type_id', related_name='clients'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
        db_column='user_id', related_name='created_clients'
    )

    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='user_updated_id', related_name='updated_clients'
    )

    have_roomate = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        db_column='have_roomate_id', related_name='roomates'
    )

    # ─────────── audit dates ───────────
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # ─────────── personal info ───────────
    first_name  = models.CharField(max_length=155)
    last_name   = models.CharField(max_length=155, blank=True)
    middle_name = models.CharField(max_length=155, blank=True)
    company     = models.CharField(max_length=155, null=True, blank=True)

    address = models.CharField(max_length=255, null=True, blank=True)
    city    = models.CharField(max_length=100, null=True, blank=True)
    state   = models.CharField(max_length=35,  null=True, blank=True)
    zip     = models.CharField(max_length=20,  null=True, blank=True)

    phone  = models.CharField(max_length=45, blank=True)
    phone2 = models.CharField(max_length=45, blank=True)
    phone3 = models.CharField(max_length=45, blank=True)
    mobile = models.CharField(max_length=45, blank=True)

    email  = models.EmailField(max_length=255, null=True, blank=True)
    email2 = models.CharField(max_length=255, blank=True)
    email3 = models.CharField(max_length=255, blank=True)

    email_maillist = models.CharField(max_length=1, blank=True)
    notes          = models.TextField(null=True, blank=True)

    gender      = models.CharField(max_length=7, blank=True)
    date_birth  = models.DateField(null=True, blank=True)

    # ─────────── emergency contact ───────────
    ems_name  = models.CharField(max_length=150, blank=True)
    ems_phone = models.CharField(max_length=50, blank=True)

    # ─────────── passport ───────────
    pp_number       = models.CharField(max_length=50, blank=True)
    pp_date_issue  = models.DateField( null=True, blank=True, default=None )
    pp_date_expire = models.DateField( null=True, blank=True, default=None )
    pp_place_issue  = models.CharField(max_length=150, blank=True)
    pp_nationality  = models.CharField(max_length=200, blank=True)

    pp_visa          = models.CharField(max_length=1, choices=YN_CHOICES, default='N')
    pp_visa_note     = models.CharField(max_length=255, blank=True)
    pp_visa_received = models.CharField(max_length=1, choices=YN_CHOICES, default='N')

    # ─────────── room preferences ───────────
    want_single_room   = models.CharField(max_length=1, blank=True)
    want_roomate       = models.CharField(max_length=1, blank=True)
    have_roomate_flag  = models.CharField(max_length=1, blank=True, db_column='have_roomate')
    have_roomate_name  = models.CharField(max_length=150, blank=True)

    # ─────────── misc flags ───────────
    registered_at_event = models.CharField(max_length=1, blank=True)
    tags                = models.CharField(max_length=255, blank=True)
    mail_lists          = models.CharField(max_length=255, blank=True)
    name_tag            = models.CharField(max_length=255, blank=True)
    from_web            = models.CharField(max_length=1, choices=YN_CHOICES, default='N')
    hearabout           = models.CharField(max_length=255, blank=True)
    unique_ident        = models.CharField(max_length=35, blank=True)

    class Meta:
        db_table = 'client'
        ordering  = ['last_name', 'first_name']
        managed   = False  # ← flip to True if Django should manage the table

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()
