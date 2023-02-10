from Car.models import *
from django.db.models import Q

class CarMgr:
    def __init__(self, car):
        self.car = car

    #Query for ALL car makes
    @staticmethod
    def getAllMakes():
        return Car.objects.order_by('make').values_list('make').distinct()

    #Query for ALL car model of specific make
    @staticmethod
    def getAllModels(_make):
        return Car.objects.filter(make = _make).order_by('model').values_list('model').distinct()

    #Query for ALL car spec of specific make and model
    @staticmethod
    def getAllSpecs(_make, _model):
        return Car.objects.filter(make = _make, model = _model).order_by('spec').values_list('spec').distinct()

    @staticmethod
    def getCars(query):
        return Car.objects.filter(
                Q(make__icontains=query) |
                Q(model__icontains=query) |
                Q(spec__icontains=query)
            )

    #Calculate and return running cost per month
    def calcCost(self, trips):
        #10 year period
        insurance = 17500 #Assuming average
        servicing = 10000 #Assuming average
        installment = self.car.installment * 12 * 10
        roadTax = self.car.roadTax * 10
        remainingValue = self.car.currentPrice - 10 * self.car.depreciation
        fuelCost = 0

        if trips != None:
            fuelType = self.car.fuelType

            if ('Petrol' in fuelType):
                fuelType = 'Petrol'
            elif ('Diesel' in fuelType):
                fuelType = 'Diesel'
            else:
                fuelType = 'Electricity'

            fuelEconomy = self.car.fuelEconomy

            if fuelEconomy == None:
                fuelEconomy = 9.7   #Based on survey average
            mileage = trips.mileage / 1000      #Mileage in terms of KM
            fuelPrice = Fuel.objects.get(fuelType=fuelType).fuelPrice
            fuelCost = fuelPrice * (mileage / 100 * fuelEconomy) * 12 * 10

        totalCost = (insurance + servicing + installment + roadTax + fuelCost - remainingValue) / (12 * 10)
        return totalCost
        
    @staticmethod
    def getCar(pk):
        return Car.objects.get(pk=pk) 

    #Getter for attributes
    def getMake():
        return self.car.make

    def getModel():
        return self.car.model

    def getSpec():
        return self.car.spec

    def getCurrentPrice():
        return self.car.currentPrice

    def getDepreciation():
        return self.car.depreciation

    def getDownPayment():
        return self.car.downPayment

    def getInstallment():
        return self.car.installment

    def getCOE():
        return self.car.COE

    def getRoadTax():
        return self.car.roadTax

    def getOMV():
        return self.car.OMV

    def getARF():
        return self.car.ARF

    def getCOEIncl():
        return self.car.COEIncl
