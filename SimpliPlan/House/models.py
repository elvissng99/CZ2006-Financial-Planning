from django.db import models
# from Main.models import *
from Finance.models import *
from Main.models import *
from multiselectfield import MultiSelectField

# Create your models here.

class HousingDataMgr(models.Manager):

    def retrieveHousingData(self,user):
        housingUserData = self.get_queryset().filter(user=user)
        housingUserData = housingUserData[0]
        return {
            "user":housingUserData.user,
            "preferredPropertyType": housingUserData.preferredPropertyType,
            "estimatedMonthlySavings": housingUserData.estimatedMonthlySavings,
            "preferredLocation": housingUserData.preferredLocation
        }
    def createHousingData(self,user,preferredPropertyType,estimatedMonthlySavings,preferredLocation):
        return self.create(user=user,
               preferredPropertyType=preferredPropertyType,
               estimatedMonthlySavings=estimatedMonthlySavings,
               preferredLocation=preferredLocation)

    def updateHousingData(self,user,preferredPropertyType,estimatedMonthlySavings,preferredLocation):
        housingUserData = self.get_queryset().filter(user=user)
        housingUserData = housingUserData[0]
        housingUserData.preferredPropertyType = preferredPropertyType
        housingUserData.estimatedMonthlySavings = estimatedMonthlySavings
        housingUserData.preferredLocation = preferredLocation
        housingUserData.save()

class HousingUserData(models.Model):
    propertyTypeList = [("1 ROOM","1 ROOM"),
                        ("2 ROOM","2 ROOM"),
                        ("3 ROOM","3 ROOM"),
                        ("4 ROOM","4 ROOM"),
                        ("5 ROOM","5 ROOM"),
                        ("EXECUTIVE", "EXECUTIVE" ),
                        ("MULTI-GENERATION", "MULTI-GENERATION")]
    locationList = [("ANG MO KIO","ANG MO KIO"),
                             ("BEDOK","BEDOK"),
                             ("BISHAN","BISHAN"),
                             ("BUKIT BATOK","BUKIT BATOK"),
                             ("BUKIT MERAH","BUKIT MERAH"),
                             ("BUKIT PANJANG","BUKIT PANJANG"),
                             ("BUKIT TIMAH","BUKIT TIMAH"),
                             ("CENTRAL AREA","CENTRAL AREA"),
                             ("CHOA CHU KANG","CHOA CHU KANG"),
                             ("CLEMENTI","CLEMENTI"),
                             ("GEYLANG","GEYLANG"),
                             ("HOUGANG","HOUGANG"),
                             ("JURONG EAST","JURONG EAST"),
                             ("JURONG WEST","JURONG WEST"),
                             ("KALLANG/WHAMPOA","KALLANG/WHAMPOA"),
                             ("MARINE PARADE","MARINE PARADE"),
                             ("PASIR RIS","PASIR RIS"),
                             ("PUNGGOL","PUNGGOL"),
                             ("QUEENSTOWN","QUEENSTOWN"),
                             ("SEMBAWANG","SEMBAWANG"),
                             ("SENGKANG","SENGKANG"),
                             ("SERANGOON","SERANGOON"),
                             ("TAMPINES","TAMPINES"),
                             ("TOA PAYOH","TOA PAYOH"),
                             ("WOODLANDS","WOODLANDS"),
                             ("YISHUN","YISHUN"),
                            ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        to_field= "username",
        default = None,
        primary_key= True
    )
    preferredPropertyType = MultiSelectField(choices=propertyTypeList, max_length=512)
    estimatedMonthlySavings = models.FloatField()
    preferredLocation = MultiSelectField(choices=locationList, max_length=512)
    housingDataMgr = HousingDataMgr()

class HousingCalculateMgr(models.Manager):
    def retrieveHousingCalculateData(self, housingUserData):
        housingCalculate= self.get_queryset().filter(housingUserData=housingUserData)
        print(housingCalculate)
        housingCalculate = housingCalculate[0]
        return {
            "maxPropertyPrice": housingCalculate.maxPropertyPrice,
            "downPayment": housingCalculate.downPayment,
            "lumpSumPayment": housingCalculate.lumpSumPayment,
            "maxHomeLoan": housingCalculate.maxHomeLoan,
            "monthlyInstallment": housingCalculate.monthlyInstallment,
            "loanPeriod": housingCalculate.loanPeriod,
        }


    def createHousingCalculateData(self,housingUserData,maxPropertyPrice,downPayment,lumpSumPayment,maxHomeLoan,monthlyInstallment,loanPeriod):
        return self.create(housingUserData = housingUserData,
               maxPropertyPrice = maxPropertyPrice,
               downPayment = downPayment,
               lumpSumPayment = lumpSumPayment,
               maxHomeLoan = maxHomeLoan,
               monthlyInstallment = monthlyInstallment,
               loanPeriod = loanPeriod)

    def updateHousingCalculateData(self,housingUserData,maxPropertyPrice,downPayment,lumpSumPayment,maxHomeLoan,monthlyInstallment,loanPeriod):
        housingCalculate = self.get_queryset().filter(housingUserData=housingUserData)
        housingCalculate = housingCalculate[0]
        housingCalculate.maxPropertyPrice = maxPropertyPrice
        housingCalculate.downPayment = downPayment
        housingCalculate.lumpSumPayment = lumpSumPayment
        housingCalculate.maxHomeLoan = maxHomeLoan
        housingCalculate.monthlyInstallment = monthlyInstallment
        housingCalculate.loanPeriod = loanPeriod
        housingCalculate.save()

    def retrieveResaleFlatPrices(self, preferredLocation, preferredPropertyType, maxPrice):
        query = self.get_queryset().filter(location = preferredLocation, flatType = preferredPropertyType, propertyPrice__lte = maxPrice)
        resaleFlatPriceList = []
        for i in query:
            resaleFlatPriceList.append([i.location, i.flatType, i.propertyPrice])
        return resaleFlatPriceList

class HousingCalculate(models.Model):
    housingUserData = models.OneToOneField(HousingUserData, primary_key = True, on_delete=models.CASCADE)
    maxPropertyPrice = models.FloatField()
    downPayment = models.FloatField()
    lumpSumPayment = models.FloatField()
    maxHomeLoan = models.FloatField()
    monthlyInstallment = models.FloatField()
    loanPeriod = models.IntegerField()
    housingCalculateMgr = HousingCalculateMgr()


class ResaleFlatPrice(models.Model):
    location = models.CharField(max_length=32)
    flatType = models.CharField(max_length=32)
    propertyPrice = models.FloatField()
    housingCalculateMgr = HousingCalculateMgr()
