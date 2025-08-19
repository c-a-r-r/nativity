# backend/users/views.py

from rest_framework import viewsets, permissions
from .models import Module, Role, Usuario
from .serializers import ModuleSerializer, RoleSerializer, UsuarioSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.usuario,
        'email': user.email,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_by_role(request):
    """Get users filtered by role (account managers vs sales agents)"""
    role = request.GET.get('role', None)
    
    if role == 'managers':
        # Get account managers (agent='NO')
        users = Usuario.objects.filter(agent='NO', activo='YES').values('id', 'nombre', 'agent')
    elif role == 'agents':
        # Get sales agents (agent='YES')
        users = Usuario.objects.filter(agent='YES', activo='YES').values('id', 'nombre', 'agent')
    else:
        # Get all active users
        users = Usuario.objects.filter(activo='YES').values('id', 'nombre', 'agent')
    
    return Response(list(users))

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAdminUser]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser]
