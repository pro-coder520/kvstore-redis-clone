from django.db import models
from django.utils import timezone


class KeyValue(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)
    value = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True, null=True, blank=True)

    def is_it_expired(self):
        """Check if the key is expired"""
        if self.expires_at and self.expires_at < timezone.now():
            return True
        return False
    
    def __str__(self):
        return f"{self.key} ({'Expired' if self.is_it_expired() else 'Active'})"