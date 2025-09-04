from django.http import HttpRequest
from datetime import datetime
from django.utils.timezone import now
import logging

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
        
        logger.info(f"Request from {ip_address} at {now()} to {path}")
        
        response = self.get_response(request)
        return response