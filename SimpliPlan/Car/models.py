from django.db import models
from Main.models import User

# Create your models here.
class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    spec = models.CharField(max_length=255)
    currentPrice = models.FloatField(null=True)
    depreciation = models.FloatField(null=True)
    downPayment = models.FloatField(null=True)
    installment = models.FloatField(null=True)
    COE = models.FloatField(null=True)
    roadTax = models.FloatField(null=True)
    OMV = models.FloatField(null=True)
    ARF = models.FloatField(null=True)
    fuelEconomy = models.FloatField(null=True)
    fuelType = models.CharField(max_length=255)
    COEIncl = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/')

    class Meta:
        unique_together = ('make', 'model', 'spec')

class Fuel(models.Model):
    fuelType = models.CharField(max_length=255, primary_key=True)
    fuelPrice = models.FloatField()

class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    frequency = models.IntegerField()
    distance = models.FloatField()

    @classmethod
    def create(cls, source, destination, frequency, distance):
        trip = cls(source=source, destination=destination, frequency=frequency, distance=distance)
        return trip


class Trips(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    trip = models.ManyToManyField('Trip')
    mileage = models.FloatField()
