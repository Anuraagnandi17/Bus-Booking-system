# myapp/management/commands/add_buses.py
from django.core.management.base import BaseCommand
from myapp.models import Bus
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Add buses automatically'

    def handle(self, *args, **options):
        cities = ['Bangalore', 'Hyderabad', 'Chennai', 'Delhi', 'Kolkata', 'Indore', 'Mumbai']

        today = datetime.now().date()

        for source in cities:
            for dest in cities:
                if source != dest:
                    for _ in range(10):
                        Bus.objects.create(
                            bus_name=f'Bus {_} - {source} to {dest}',
                            source=source,
                            dest=dest,
                            nos=100,
                            rem=random.randint(1, 99),
                            price=round(random.uniform(15.0, 50.0), 2),
                            date=today,
                            time='12:00',
                        )

        self.stdout.write(self.style.SUCCESS('Buses added successfully'))
