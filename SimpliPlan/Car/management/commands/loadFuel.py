import csv
from django.core.management import BaseCommand

from Car.models import Fuel

class Command(BaseCommand):
    help = "Loads fuel prices from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        Fuel.objects.all().delete()
        file_path = options["file_path"]

        with open(file_path, "r") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            fuel = []

            for row in data:
                fields = row
                fuel.append(Fuel(fuelType=fields[0], fuelPrice=float(fields[1])))

            if fuel:
                Fuel.objects.bulk_create(fuel)
        self.stdout.write("Successfully added fuel type and prices", ending='')
