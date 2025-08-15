from rest_framework import viewsets
from .models import Quote, ItineraryCity
from .serializers import QuoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import DestinationGroup, Destination
from .serializers import DestinationGroupSerializer, DestinationSerializer, ItineraryCitySerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import re



class QuotePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per'
    max_page_size = 100

class QuoteViewSet(viewsets.ModelViewSet):
    def update(self, request, *args, **kwargs):
        print('DEBUG: Update request.data:', request.data)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        print('DEBUG: Partial update request.data:', request.data)
        return super().partial_update(request, *args, **kwargs)
    queryset = Quote.objects.all().order_by('id')
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = QuotePagination

    STATUS_SLUG_TO_ID = {
        "draft":             1,
        "sent-to-contact":   2,
        "accepted":          4,
        "rejected":          5,
        "completed":         6,
        # Add more as needed
    }

    def get_queryset(self):
        qs = super().get_queryset().order_by('-date_created')  # Default ordering: newest first

        # 1. Status filter
        slug = (self.request.GET.get("status") or "all").lower().strip()
        if slug != "all":
            status_id = self.STATUS_SLUG_TO_ID.get(slug)
            if status_id is not None:
                qs = qs.filter(quote_status_id=status_id)
            else:
                return Quote.objects.none()

        # 2. Workflow status filter
        workflow_status = self.request.GET.get("workflow_status")
        if workflow_status:
            try:
                workflow_id = int(workflow_status)
                qs = qs.filter(workflow_status_rel=workflow_id)
            except ValueError:
                pass

        # 3. Search filter
        term = (self.request.GET.get("q") or "").strip()
        if term:
            filters = (
                Q(trip_name__icontains=term) |
                Q(church_name__icontains=term)
            )
            # If you have a related client model with a name field:
            # Uncomment the next line if you want to search by client name:
            # filters = filters | Q(client__name__icontains=term)
            m = re.match(r"^(?:np-)?(\d+)$", term, re.I)
            if m:
                try:
                    filters = filters | Q(id=int(m.group(1)))
                except ValueError:
                    pass
            qs = qs.filter(filters)

        return qs
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def destination_group_list(request):
    groups = DestinationGroup.objects.all()
    return Response(DestinationGroupSerializer(groups, many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def destination_list(request):
    dests = Destination.objects.all()
    return Response(DestinationSerializer(dests, many=True).data)    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def itinerary_city_list(request):
    cities = ItineraryCity.objects.all()
    return Response(ItineraryCitySerializer(cities, many=True).data)