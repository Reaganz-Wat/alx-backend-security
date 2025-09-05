from django.core.management import BaseCommand
from ...models import Task

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("task", type=str, help="Enter a task to add into db")
    
    def handle(self, *args, **options):
        task = options["task"]
        
        Task.objects.create(description=task)
        
        self.stdout.write(f"Task added: {task}")