"""
from rest_framework import serializers


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(label="Refresh Token")


class AccessTokenSerializer(serializers.Serializer):
    access = serializers.CharField(label="Access Token")
"""
