from django.http import HttpRequest, HttpResponse
from datetime import datetime
import logging
import requests
from django.core.cache import cache
from .models import RequestLog, BlockedIP

logger = logging.getLogger(__name__)
GEO_CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours

class IPGeolocationMiddleware:
    """
    Middleware that:
    1. Blocks requests from blacklisted IPs
    2. Fetches geolocation (country/city) from cache or API
    3. Logs requests with geolocation
    """
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("IPGeolocationMiddleware initialized")

    def __call__(self, request: HttpRequest):
        ip_address = request.META.get("REMOTE_ADDR", "127.0.0.1")

        # --- Check if IP is blocked ---
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponse("Your IP Address is blocked", status=403)

        # --- Fetch geolocation from cache ---
        geo = cache.get(f"geo:{ip_address}")
        if not geo:
            try:
                response = requests.get(f"https://ipapi.co/{ip_address}/json/")
                data = response.json()
                geo = {
                    "country": data.get("country_name", ""),
                    "city": data.get("city", "")
                }
            except Exception:
                geo = {"country": "", "city": ""}

            # Save to Redis cache for 24h
            cache.set(f"geo:{ip_address}", geo, GEO_CACHE_TIMEOUT)

        # --- Log the request ---
        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.get_full_path(),
            country=geo["country"],
            city=geo["city"],
            timestamp=datetime.now()
        )
        logger.info(f"Request from {ip_address} to {request.get_full_path()} | Geo: {geo}")

        response = self.get_response(request)
        return response