from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import CustomerUser, CustomerProfile, EmailVerificationToken, PasswordResetToken
from .serializers import (
    CustomerRegistrationSerializer, CustomerLoginSerializer,
    CustomerUserSerializer, CustomerProfileSerializer,
    PasswordChangeSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)


class CustomerRegistrationView(generics.CreateAPIView):
    """
    Customer registration endpoint
    """
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create user
        user = serializer.save()
        
        # Generate email verification token
        token = secrets.token_urlsafe(50)
        expires_at = timezone.now() + timedelta(hours=24)
        
        EmailVerificationToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # TODO: Send verification email (temporarily disabled due to SMTP config)
        # self.send_verification_email(user, token)
        
        return Response({
            'message': 'Registration successful. You can now sign in.',
            'user': CustomerUserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    def send_verification_email(self, user, token):
        """Send email verification email"""
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        
        subject = 'Verify your Nativity Pilgrimage account'
        message = f'''
        Dear {user.first_name},
        
        Thank you for registering with Nativity Pilgrimage!
        
        Please click the link below to verify your email address:
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create this account, please ignore this email.
        
        Blessings,
        Nativity Pilgrimage Team
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class CustomerLoginView(generics.GenericAPIView):
    """
    Customer login endpoint
    """
    serializer_class = CustomerLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        return Response({
            'message': 'Login successful',
            'user': CustomerUserSerializer(user).data
        })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def customer_logout(request):
    """
    Customer logout endpoint
    """
    try:
        # Delete the user's token
        request.user.auth_token.delete()
    except:
        pass
    
    return Response({'message': 'Logout successful'})


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    """
    Customer profile view/update endpoint
    """
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile


class CustomerAccountView(generics.RetrieveUpdateAPIView):
    """
    Customer account information view/update endpoint
    """
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """
    Change customer password
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Delete all existing tokens to force re-login
        Token.objects.filter(user=user).delete()
        
        return Response({'message': 'Password changed successfully'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_password_reset(request):
    """
    Request password reset
    """
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = CustomerUser.objects.get(email=email)
        
        # Generate reset token
        token = secrets.token_urlsafe(50)
        expires_at = timezone.now() + timedelta(hours=2)
        
        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # Send reset email
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        
        subject = 'Reset your Nativity Pilgrimage password'
        message = f'''
        Dear {user.first_name},
        
        You requested to reset your password for your Nativity Pilgrimage account.
        
        Please click the link below to reset your password:
        {reset_url}
        
        This link will expire in 2 hours.
        
        If you didn't request this password reset, please ignore this email.
        
        Blessings,
        Nativity Pilgrimage Team
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return Response({'message': 'Password reset email sent'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def confirm_password_reset(request):
    """
    Confirm password reset with token
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)
    
    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                is_used=False
            )
            
            if reset_token.is_expired():
                return Response(
                    {'error': 'Reset token has expired'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Reset password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            # Delete all existing tokens to force re-login
            Token.objects.filter(user=user).delete()
            
            return Response({'message': 'Password reset successful'})
            
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Invalid reset token'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_email(request, token):
    """
    Verify email address with token
    """
    try:
        verification_token = EmailVerificationToken.objects.get(
            token=token,
            is_used=False
        )
        
        if verification_token.is_expired():
            return Response(
                {'error': 'Verification token has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify email
        user = verification_token.user
        user.is_email_verified = True
        user.save()
        
        # Mark token as used
        verification_token.is_used = True
        verification_token.save()
        
        return Response({'message': 'Email verified successfully'})
        
    except EmailVerificationToken.DoesNotExist:
        return Response(
            {'error': 'Invalid verification token'},
            status=status.HTTP_400_BAD_REQUEST
        )
