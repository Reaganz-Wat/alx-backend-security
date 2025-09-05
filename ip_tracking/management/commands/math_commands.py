from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Please this is a sample of a help command"
    
    def add_arguments(self, parser):
        parser.add_argument("numbers", nargs="+", type=str, help="One or more arguments")
    
    def handle(self, *args, **options):
        numbers = [int(n) for n in options["numbers"]]
        
        number_of_items = len(numbers)
        
        sum = 0
        
        for number in numbers:
            sum += int(number)
            
        average = sum / number_of_items
        
        max_number = max(numbers)
        min_number = min(numbers)
        
        print_output = f"""
        You entered {number_of_items} numbers
        Sum = {sum}
        Average = {average}
        Max = {max_number}
        Min = {min_number}
        """
        
        self.stdout.write(print_output)