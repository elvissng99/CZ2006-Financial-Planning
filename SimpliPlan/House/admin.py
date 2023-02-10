from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(HousingCalculate)
admin.site.register(HousingUserData)
admin.site.register(ResaleFlatPrice)