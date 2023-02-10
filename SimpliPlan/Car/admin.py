from django.contrib import admin
from .models import *

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'spec', 'currentPrice', 'depreciation', 'downPayment',
                    'installment', 'COE', 'roadTax', 'OMV', 'ARF', 'fuelEconomy', 'fuelType', 'COEIncl', 'image')

class FuelAdmin(admin.ModelAdmin):
    list_display = ('fuelType', 'fuelPrice')

class TripAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'frequency', 'distance')

class TripsAdmin(admin.ModelAdmin):
    list_display = ('User', 'mileage')

admin.site.register(Car, CarAdmin)
admin.site.register(Fuel, FuelAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Trips, TripsAdmin)
