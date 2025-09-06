from django.core.management.base import BaseCommand
from ...models import BlockedIP

class Command(BaseCommand):
    help = "Unblock an IP address"

    def add_arguments(self, parser):
        parser.add_argument(
            "blocked_ip", type=str, help="Input the blocked IP Address"
        )

    def handle(self, *args, **options):
        blocked_ip = options["blocked_ip"]

        blocked_qs = BlockedIP.objects.filter(ip_address=blocked_ip)

        if blocked_qs.exists():
            blocked_qs.delete()
            self.stdout.write(self.style.SUCCESS(f"IP {blocked_ip} unblocked successfully"))
        else:
            self.stdout.write(self.style.SUCCESS(f"IP {blocked_ip} is not blocked"))
