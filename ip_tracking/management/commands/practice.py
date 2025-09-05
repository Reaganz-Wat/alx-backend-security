from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="One or more arguments")

    def handle(self, *args, **options):
        ip_address = options["ip_address"]  # This will be a list
        
        self.stdout.write(f"IP Address added: {ip_address}")