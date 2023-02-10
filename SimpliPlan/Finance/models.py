from django.db import models
from Main.models import *
# Create your models here.

class Information(models.Model):
    DOB = models.DateField()
    gender = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    maritalStatus = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    monthlyIncome = models.FloatField()
    spouseMonthlyIncome = models.FloatField()
    noOfDependents = models.IntegerField()
    OAAmount = models.FloatField()
    SAAmount = models.FloatField()
    medisave = models.FloatField()
    user = models.OneToOneField(
        User,
        to_field="username",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
class OtherIncomeSource(models.Model):
    incomeSource = models.CharField(max_length=255)
    amount = models.FloatField()
    information = models.ForeignKey(Information, on_delete=models.CASCADE)


class Debt(models.Model):
    debtName = models.CharField(max_length=255)
    amount = models.FloatField()
    repayment = models.FloatField()
    interest = models.FloatField()
    information = models.ForeignKey(Information, on_delete=models.CASCADE)

class Asset(models.Model):
    assetName = models.CharField(max_length=255)
    amount = models.FloatField()
    returns = models.FloatField()
    information = models.ForeignKey(Information, on_delete=models.CASCADE)

class MonthlyExpense(models.Model):
    expenseName = models.CharField(max_length=255)
    amount = models.FloatField()
    information = models.ForeignKey(Information, on_delete=models.CASCADE)

class IncomeQuartile(models.Model):
    quartile = models.IntegerField(primary_key=True)
    averageIncome = models.FloatField()
    averageExpenditure = models.FloatField()
    
class AverageIndividual(models.Model):
    meanIncome = models.FloatField()
    meanExpense = models.FloatField()
