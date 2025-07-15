from rest_framework import viewsets, filters
from .models import Client
from .serializers import ClientSerializer
from rest_framework.permissions import IsAuthenticated

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('last_name', 'first_name')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'first_name', 'last_name', 'email', 'email2', 'email3',
        'phone', 'phone2', 'phone3', 'mobile', 'company', 'address',
        'city', 'state', 'zip', 'tags', 'mail_lists', 'name_tag',
        'from_web', 'hearabout', 'unique_ident', 'email_maillist'
    ]