from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    access = serializers.SerializerMethodField(label="ID компании")
    refresh = serializers.SerializerMethodField(label="Токен обновления")

    def get_access(self, obj):
        return obj.access_token

    def get_refresh(self, obj):
        return obj.refresh_token
