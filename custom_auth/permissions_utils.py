from .models import Resource, AccessRules


def has_permission(user, resource_name, action):

    if not user or not user.is_active:
        return False

    try:
        resource = Resource.objects.get(name=resource_name)
        access_rule = AccessRules.objects.get(role=user.role, resource=resource)
    except (Resource.DoesNotExist, AccessRules.DoesNotExist):
        return False

    if action == 'read':
        return access_rule.read_all_permission or access_rule.read_permission
    if action == 'create':
        return access_rule.create_permission
    if action == 'update':
        return access_rule.update_all_permission or access_rule.update_permission
    if action == 'delete':
        return access_rule.delete_all_permission or access_rule.delete_permission

    return False
