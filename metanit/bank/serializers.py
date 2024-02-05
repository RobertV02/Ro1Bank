from rest_framework import serializers

from .models import Check


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'