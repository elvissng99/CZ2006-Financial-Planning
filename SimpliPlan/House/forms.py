# from django import forms
# from .models import *
# from multiselectfield import MultiSelectFormField

# class HousingUserDataForm(forms.Form):
#     propertyType = MultiSelectField(choices=HousingUserData.propertyTypeList)
#     #propertyType = forms.CharField(max_length=32)
#     estimatedMonthlySavings = forms.IntegerField()
#     preferredLocation = MultiSelectField(choices=HousingUserData.locationList)


# class HousingCalculateForm(forms.Form):
#     maxPropertyPrice = forms.IntegerField()
#     downPayment = forms.DecimalField(max_digits=16, decimal_places=2)
#     lumpSumPayment = forms.DecimalField(max_digits=16, decimal_places=2)
#     maxHomeLoan = forms.DecimalField(max_digits=16, decimal_places=2)
#     monthlyInstallment = forms.DecimalField(max_digits=16, decimal_places=2)
#     loanPeriod = forms.IntegerField()
