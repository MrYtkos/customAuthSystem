from django.db import models

from .role import Role


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, blank=True, null=True)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def save(self, *args, **kwargs):
        if not self.role:
            try:
                self.role_id = Role.objects.get(name="user")
            except Role.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} {self.role}"

