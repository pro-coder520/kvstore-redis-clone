from django.core.management.base import BaseCommand
from django.utils import timezone
from store.models import KeyValue

class Command(BaseCommand):
    help = 'Deletes all expired keys from the database to free up memory'
    def handle(self, *args, **kwargs):
        now = timezone.now()
        count, _ = KeyValue.objects.filter(expires_at__lt=now).delete() # Bulk delete
        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} expired keys."))
