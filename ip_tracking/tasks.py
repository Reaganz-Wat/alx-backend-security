from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from .models import RequestLog, SuspiciousIP


@shared_task
def detect_suspicious_ips():
    """Hourly task to flag suspicious IPs"""
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1. IPs exceeding 100 requests/hour
    heavy_hitters = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(request_count=Count("id"))
        .filter(request_count__gt=100)
    )

    for entry in heavy_hitters:
        ip = entry["ip_address"]
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason=f"Excessive requests: {entry['request_count']} in last hour"
        )

    # 2. IPs accessing sensitive paths
    sensitive_paths = ["/admin", "/login"]

    suspicious_access = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago, path__in=sensitive_paths
    ).values_list("ip_address", flat=True).distinct()

    for ip in suspicious_access:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason="Accessed sensitive path"
        )
