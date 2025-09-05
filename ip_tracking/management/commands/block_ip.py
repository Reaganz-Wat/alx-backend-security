from django.core.management import BaseCommand
from ...models import BlockedIP

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="Enter the IP Address")
    
    def handle(self, *args, **options):
        ip_address = options["ip_address"]
        
        # Insert into BlockedIP Address
        BlockedIP.objects.create(ip_address=ip_address)
        
        self.stdout.write(f"IP Address {ip_address} blocked")