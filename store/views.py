import json
import logging
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from .models import KeyValue

logger = logging.getLogger(__name__) # This sets up the logger

@method_decorator(csrf_exempt, name='dispatch')
class KVStore(View):
    """
    This is the main entry point for the key-value store
    It supports GET (Retrieve) and POST (Set)
    """
    def get(self, request, key):
        """
        GET /<key>
        Retrieves the value tied to the key, performs lazy expiration.
        """
        try:
            item = KeyValue.objects.get(key=key)
            if item.is_it_expired():
                logger.info(f"Key '{key} unusable due to expiration. Deleting.")
                item.delete()
                return JsonResponse({"error": "Nonexistent/expired key"}, status=404)
            return JsonResponse({
                "key": item.key,
                "value": item.value, 
                "ttl_remaining": self._get_ttl(item)
            })
        except KeyValue.DoesNotExist:
            return JsonResponse({"error": "Key could not be found"}, status=404)
    
    def post (self, request, key):
        """
        POST /<key>
        Body: {"value": <any>, "ttl": <seconds (int, optional)>}
        Sets the value. Overwrites key if it exists.
        """
        try:
            data = json.loads(request.body)
            value = data.get('value')
            ttl_seconds = data.get('ttl', None)

            if value is None:
                return JsonResponse({"error": "Missing value in payload"}, status=400)
            
            # Calculate expiry date of key
            expires_at = None
            if ttl_seconds:
                expires_at = timezone.now() + timedelta(seconds=int(ttl_seconds))
            
            # Handles race conditions at the database level
            obj, created = KeyValue.objects.update_or_create(
                key=key,
                defaults={
                    "value": value,
                    "expires_at": expires_at,
                }
            )

            action = "created" if created else "updated"
            return JsonResponse({
                "status": "ok",
                "action": action,
                "key": key,
                "expires_at": expires_at,
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error setting key '{key}': {str(e)}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)

    def _get_ttl(self, item):
        """Helper to fetch remaining seconds"""
        if not item.expires_at():
            return -1 # Standard Redis code for "no expiration"
        delta = item.expires_at() - timezone.now()
        return max(0, int(delta.total_seconds()))