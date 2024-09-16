from rest_framework import serializers

from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_active', 'is_staff', 'is_superuser')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []


class CustomTokenSerializer(serializers.Serializer):
    phone    = serializers.CharField()
    password = serializers.CharField(required=False)


class OTPSerializer(serializers.Serializer):
    otp   = serializers.CharField()
    phone = serializers.CharField()
