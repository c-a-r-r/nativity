# backend/users/serializers.py

from rest_framework import serializers
from .models import Module, Role, Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'usuario'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Module
        fields = ['id', 'nombre']


class RoleSerializer(serializers.ModelSerializer):
    modules = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Module.objects.all()
    )

    class Meta:
        model  = Role
        fields = ['id', 'nombre', 'modules']


class UsuarioSerializer(serializers.ModelSerializer):
    grupo = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        allow_null=True
    )
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model  = Usuario
        fields = [
            'id', 'usuario', 'password', 'email', 'grupo',
            'activo', 'nombre', 'u_first_name', 'u_last_name',
            'telefono_fijo', 'telefono_movil', 'comision', 'agent',
        ]
        extra_kwargs = {
            'usuario': {'required': True},
        }

    def create(self, validated_data):
        pwd = validated_data.pop('password', None)
        user = super().create(validated_data)
        if pwd:
            user.set_password(pwd)
            user.save(update_fields=['password'])
        return user

    def update(self, instance, validated_data):
        pwd = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if pwd:
            user.set_password(pwd)
            user.save(update_fields=['password'])
        return user