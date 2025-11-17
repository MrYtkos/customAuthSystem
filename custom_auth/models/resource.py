from django.db import models

from .user import User


class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

