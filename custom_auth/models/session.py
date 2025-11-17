from django.db import models
from django.utils import timezone

from .user import User


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"Session (user={self.user.email}, expires_at: {self.expires_at})"
