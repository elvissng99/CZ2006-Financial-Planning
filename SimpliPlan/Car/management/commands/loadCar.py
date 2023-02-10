import csv
from django.core.management import BaseCommand

from Car.models import Car

class Command(BaseCommand):
    help = "Loads cars from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        Car.objects.all().delete()
        file_path = options["file_path"]

        with open(file_path, "r") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            cars = []
            next(data)

            for row in data:
                fields = row

                for i in range(len(fields)):
                    if fields[i] == '-' or fields[i] == 'POA' or fields[i] == '':
                        fields[i] = None

                    if fields[i] == 'TRUE':
                        fields[i] = True

                    if fields[i]=='FALSE':
                        fields[i] = False

                #Check if depreciation, installment, roadTax not existent and COE not included
                if (fields[6] == None or fields[8] == None or fields[10] == None or fields[15] == False):
                    continue


                car = Car(
                    make = fields[2],
                    model = fields[3],
                    spec = fields[4],
                    currentPrice = fields[5],
                    depreciation = fields[6],
                    downPayment = fields[7],
                    installment = fields[8],
                    COE = fields[9],
                    roadTax = fields[10],
                    OMV = fields[11],
                    ARF = fields[12],
                    fuelEconomy = fields[13],
                    fuelType = fields[14],
                    COEIncl = fields[15],
                    image = "images/Lexus_LC_500_O7P2Cpu_pbv674W.jpg"
                )

                cars.append(car)

            if cars:
                Car.objects.bulk_create(cars)
        self.stdout.write("Successfully added cars", ending='')
