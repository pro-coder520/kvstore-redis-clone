import json
import logging
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
    