from django.db import models

from .role import Role
from .resource import Resource


class AccessRules(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)

    create_permission = models.BooleanField(default=False)

    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)

    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = (('role_id', 'resource_id'),)
