from django.http import HttpRequest, HttpResponseForbidden
from datetime import datetime
import logging
from .models import RequestLog, BlockedIP

logger = logging.getLogger(__name__)

class LogHeadersMiddlware():
    def __init__(self, get_response):
        print(f"Starting middlware...")
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest):
        print("Calling middlware...")
        
        ip_address = request.META['REMOTE_ADDR']
        timestamp = datetime.now()
        path = request.get_full_path()
        
        RequestLog.objects.create(ip_address=ip_address, path=path)
        
        logger.info(f"Request from {ip_address} at {timestamp} to {path}")
        
        response = self.get_response(request)
        return response
    
class BlockIP():
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request: HttpRequest):
        
        ip_addr = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
        
        if BlockedIP.objects.filter(ip_address=ip_addr).exists():
            return HttpResponseForbidden("Your IP Address blocked")
        
        response = self.get_response(request)
        
        return response