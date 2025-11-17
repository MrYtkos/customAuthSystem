from rest_framework import serializers

from custom_auth.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_id', 'resource_name']
