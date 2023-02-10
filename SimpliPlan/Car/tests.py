from django.test import TestCase
from .carMgr import *
from .models import Car
from .tripMgr import *
import csv

# Create your tests here.
class CarTestCase(TestCase):
    def setUp(self):
        file_path = 'Car/cars.csv'
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
                    COEIncl = fields[15]
                )

                cars.append(car)

            if cars:
                Car.objects.bulk_create(cars)


    def test(self):
        for make in CarMgr.getAllMakes():
            print(make)

        for model in CarMgr.getAllModels('Mercedes-Benz'):
            print(model)

        for spec in CarMgr.getAllSpecs('Mercedes-Benz', 'Mercedes-Benz E-Class Saloon'):
            print(spec)

class TripTestCase(TestCase):
    def setUp(self):
        self.tripMgr = TripMgr()
        self.user=User(username="test", password="test", email="test@test.com")
        self.user.save()


    def test(self):
        #Test adding trips for new user
        source = ["Choa Chu Kang", "Yew Tee", "Changi"]
        destination = "NTU"
        for i in source:
            self.tripMgr.addTrip(i, destination, 2)
        self.tripMgr.deleteTrip(1)
        self.tripMgr.addTripDB()
        self.tripMgr.addUserTripDB(self.user)
        trips = self.tripMgr.getUserTripDB(self.user)

        #Test updating trip
        self.tripMgr.addTrip("Bukit Batok", "Changi", 2)
        self.tripMgr.addTripDB()
        self.tripMgr.addUserTripDB(self.user)
        trips = self.tripMgr.getUserTripDB(self.user)



class carCostTestCase(TestCase):
    def setUp(self):
        file_path = 'Car/cars.csv'
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
                    COEIncl = fields[15]
                )

                cars.append(car)

            if cars:
                Car.objects.bulk_create(cars)

        file_path = 'Car/fuel.csv'

        with open(file_path, "r") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            fuel = []

            for row in data:
                fields = row
                fuel.append(Fuel(fuelType=fields[0], fuelPrice=float(fields[1])))

            if fuel:
                Fuel.objects.bulk_create(fuel)

        self.user=User(username="test", password="test", email="test@test.com")
        self.user.save()



    def test(self):
        tripMgr = TripMgr()
        car = Car.objects.get(make = 'Audi', model = 'Audi A5 Sportback Mild Hybrid', spec = '2.0 TFSI S tronic (A)')
        carMgr = CarMgr(car)

        #Test adding trips for new user
        source = ["Choa Chu Kang", "Yew Tee", "Changi"]
        destination = "NTU"
        for i in source:
            tripMgr.addTrip(i, destination, 2)
        tripMgr.addTripDB()
        tripMgr.addUserTripDB(self.user)
        trips = tripMgr.getUserTripDB(self.user)
        totalCost = carMgr.calcCost(Trips.objects.get(User = self.user))
        print(totalCost)
