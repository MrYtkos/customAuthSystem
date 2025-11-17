from rest_framework import serializers

from custom_auth.models import AccessRules


class AccessRulesSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role_name', read_only=True)
    resource_name = serializers.CharField(source='resource_name', read_only=True)

    class Meta:
        model = AccessRules
        fields = [
            'id',
            'role',
            'role_name',
            'resource',
            'resource_name',
            'read_permission',
            'read_all_permission',
            'create_permission',
            'update_permission',
            'update_all_permission',
            'delete_permission',
            'delete_all_permission',
        ]
