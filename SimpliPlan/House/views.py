import csv
import os
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from Finance.models import *
from Finance.FinanceMgr import *

# Create your views here.
# def houseInsertUserData_view(request):
#     form = HousingUserDataForm()
#     if request.method == "POST":
#         form = HousingUserDataForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             HousingUserData.objects.create(**form.cleaned_data)
#         else:
#             print(form.errors)
#     context = {
#         "form" : form
#     }
#     return render(request, "houseInsertUserData.html", context)

# def houseInsertHousingCalculate_view(request):
#     form = HousingCalculateForm()
#     if request.method == "POST":
#         form = HousingCalculateForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             HousingCalculate.objects.create(**form.cleaned_data)
#         else:
#             print(form.errors)
#     context = {
#         "form" : form
#     }
#     return render(request, "houseInsertHousingCalculate.html", context)


def form_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.user.get(username=username)
        financeMgr = FinanceMgr(user)
        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        context = {"username": username, "firstTime": firstTime}

        try:
            user.information
            if(user.information.debt_set.all().filter(debtName="House").exists()):
                context["estimatedMonthlySavings"] = financeMgr.calculateCashFlow(
                ) + user.information.debt_set.all().filter(debtName="House")[0].repayment
            else:
                context["estimatedMonthlySavings"] = financeMgr.calculateCashFlow()

        except:
            context["estimatedMonthlySavings"] = -1

        if request.method == "POST":
            if(request.POST):
                # user = User.user.validate("Main_user2","main12345")

                towns = request.POST.getlist("towns[]")
                estimatedMonthlySavings = request.POST.get(
                    "estimatedMonthlySavings")
                propertyTypes = request.POST.getlist("propertyType[]")

                # assuming housing loan instead of bank loan
                # 90% of maxPropertyPrice can be loaned, 10% downpayment
                monthlyInstallment = float(estimatedMonthlySavings)
                interestRate_annual = 0.026
                monthlyInterestRate = interestRate_annual/12
                loanPeriod = 25  # maximum 25
                maxHomeLoan = monthlyInstallment*(((1 + monthlyInterestRate)**(loanPeriod*12)-1) /
                                                  (monthlyInterestRate*(1+monthlyInterestRate)**(loanPeriod*12)))
                maxPropertyPrice = (100/90) * maxHomeLoan
                downPayment = 0.1*maxPropertyPrice
                if "4 ROOM" or "5 ROOM" or "EXECUTIVE" or "MULTI-GENERATION" in propertyTypes:
                    optionFee = 2000
                elif "3 ROOM" in propertyTypes:
                    optionFee = 1000
                else:
                    optionFee = 500
                # 1% first 180k, 2% next 180k, 3% next 640k, 4% remaining
                if maxPropertyPrice < 180000:
                    stampDuty = 0.01 * maxPropertyPrice
                else:
                    stampDuty = 0.01 * 180000
                    remainingPropertyPrice = maxPropertyPrice - 180000
                    if(remainingPropertyPrice < 180000):
                        stampDuty += 0.02*remainingPropertyPrice
                    else:
                        stampDuty += 0.02*180000
                        remainingPropertyPrice -= 180000
                        if (remainingPropertyPrice < 640000):
                            stampDuty += 0.03 * remainingPropertyPrice
                        else:
                            stampDuty += 0.03 * 640000
                            remainingPropertyPrice -= 640000
                            stampDuty += 0.04 * remainingPropertyPrice
                lumpSumPayment = downPayment + optionFee + stampDuty

                try:
                    # will give error if housinguserdata does not exist yet
                    housingUserData = user.housinguserdata
                    HousingUserData.housingDataMgr.updateHousingData(user=user,
                                                                     preferredPropertyType=propertyTypes,
                                                                     estimatedMonthlySavings=estimatedMonthlySavings,
                                                                     preferredLocation=towns)
                    # housingUserData.preferredPropertyType = propertyTypes
                    # housingUserData.estimatedMonthlySavings = estimatedMonthlySavings
                    # housingUserData.preferredLocation = towns
                    # housingUserData.save()

                    HousingCalculate.housingCalculateMgr.updateHousingCalculateData(housingUserData=housingUserData,
                                                                                    maxPropertyPrice=maxPropertyPrice,
                                                                                    downPayment=downPayment,
                                                                                    lumpSumPayment=lumpSumPayment,
                                                                                    maxHomeLoan=maxHomeLoan,
                                                                                    monthlyInstallment=monthlyInstallment,
                                                                                    loanPeriod=loanPeriod)

                    #housingCalculate = housingUserData.housingcalculate
                    # housingCalculate.maxPropertyPrice = maxPropertyPrice
                    # housingCalculate.downPayment = downPayment
                    # housingCalculate.lumpSumPayment = lumpSumPayment
                    # housingCalculate.maxHomeLoan = maxHomeLoan
                    # housingCalculate.monthlyInstallment = monthlyInstallment
                    # housingCalculate.loanPeriod = loanPeriod
                    # housingCalculate.save()
                except:
                    # creating
                    housingUserData = HousingUserData.housingDataMgr.createHousingData(user=user,
                                                                                       preferredPropertyType=propertyTypes,
                                                                                       estimatedMonthlySavings=estimatedMonthlySavings,
                                                                                       preferredLocation=towns)

                    HousingCalculate.housingCalculateMgr.createHousingCalculateData(housingUserData=housingUserData,
                                                                                    maxPropertyPrice=maxPropertyPrice,
                                                                                    downPayment=downPayment,
                                                                                    lumpSumPayment=lumpSumPayment,
                                                                                    maxHomeLoan=maxHomeLoan,
                                                                                    monthlyInstallment=monthlyInstallment,
                                                                                    loanPeriod=loanPeriod)
                    # HousingUserData.objects.create(user=user,
                    #                                                  preferredPropertyType=propertyTypes,
                    #                                                  estimatedMonthlySavings=estimatedMonthlySavings,
                    #                                                  preferredLocation=towns)

                    # HousingCalculate.objects.create(housingUserData = housingUserData,
                    #                                                                 maxPropertyPrice = maxPropertyPrice,
                    #                                                                 downPayment = downPayment,
                    #                                                                 lumpSumPayment = lumpSumPayment,
                    #                                                                 maxHomeLoan = maxHomeLoan,
                    #                                                                 monthlyInstallment = monthlyInstallment,
                    #                                                                 loanPeriod = loanPeriod)
                finally:
                    return redirect('/house/costBreakdown/')

        return render(request, 'house/form.html', context)
    else:
        return redirect('home')


def costBreakdown_view(request):
    if request.session.has_key('username'):

        username = request.session['username']

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        # Query database
        user = User.user.get(username=username)
        try:
            # will give error if housinguserdata does not exist yet
            user.housinguserdata
            financeMgr = FinanceMgr(user)
            if(request.POST):
                try:
                    user.information
                    financeMgr = FinanceMgr(user)
                    if(user.information.debt_set.all().filter(debtName="House").exists()):
                        financeMgr.updateDebt(user.information.debt_set.all().filter(debtName="House")[0].id,
                                              "House",  request.POST.get("price"), request.POST.get("repayment"), 0.026)
                    else:
                        financeMgr.createDebt("House", request.POST.get("price"),
                                              request.POST.get("repayment"), 0.026)
                    if(user.information.asset_set.all().filter(assetName="House").exists()):
                        financeMgr.updateAsset(user.information.asset_set.all().filter(assetName="House")[0].id,
                                               "House", request.POST.get("price"), 0)
                    else:
                        financeMgr.createAsset(
                            "House", request.POST.get("price"), 0)
                    return redirect("/finance/balanceSheet_Result/")
                except:
                    return redirect("/finance/questionaire/")

            else:
                userData = user.housinguserdata
                housingCalculate = HousingCalculate.housingCalculateMgr.retrieveHousingCalculateData(
                    userData)
                userData = HousingUserData.housingDataMgr.retrieveHousingData(
                    user)
                # User prefered location and type
                preferredPropertyType = userData['preferredPropertyType']
                preferredLocation = userData['preferredLocation']

                # User prefered location and type
                preferredPropertyType = userData['preferredPropertyType']
                preferredLocation = userData['preferredLocation']

                # Get list of resale properties for all permutations of type and location
                resaleList = []
                # workpath = os.path.dirname(os.path.abspath(__file__))
                # with open(os.path.join(workpath, 'resale-flat-prices-2021.csv'), 'r') as csv_file:
                #     reader = csv.reader(csv_file)
                #     for row in reader:
                #         if (row[1] in preferredLocation and row[2] in preferredPropertyType and float(row[3]) <= housingCalculate['maxPropertyPrice']):
                #             resaleList.append([row[1], row[2], float(row[3])])
                for i in preferredPropertyType:
                    for j in preferredLocation:
                        resaleList += ResaleFlatPrice.housingCalculateMgr.retrieveResaleFlatPrices(
                            j, i, housingCalculate['maxPropertyPrice'])

                # Sort the list of resale properties by price
                resaleList = sorted(resaleList, key=lambda x: x[2])
                mostAffordable = resaleList[0]
                maxAffordable = resaleList[-1]
                suggestedProperties = []
                for i in [mostAffordable, maxAffordable]:
                    dictionary = {}
                    dictionary['location'] = i[0]
                    dictionary['type'] = i[1]
                    price = i[2]
                    dictionary['price'] = price

                    # MonthlyInstallment
                    maxLTV = 0.90 * price
                    dictionary["maxLTV"] = maxLTV
                    interestRate_annual = 0.026
                    interestRate_monthly = 0.026 / 12
                    periods = 12 * 25  # Assume 25 years
                    dictionary['period'] = 25
                    monthlyInstallment = (maxLTV * (interestRate_monthly * (1 + interestRate_monthly) ** periods) /
                                          ((1 + interestRate_monthly) ** periods - 1))
                    dictionary['monthlyInstallment'] = round(
                        monthlyInstallment, 1)

                    downPayment = 0.10 * price
                    dictionary['downPayment'] = downPayment

                    if "4 ROOM" or "5 ROOM" or "EXECUTIVE" or "MULTI-GENERATION" in propertyTypes:
                        optionFee = 2000
                    elif "3 ROOM" in propertyTypes:
                        optionFee = 1000
                    else:
                        optionFee = 500

                    # Buyer stamp duties
                    if price < 180000:
                        stampDuty = 0.01 * price
                    else:
                        stampDuty = 0.01 * 180000
                        remainingPropertyPrice = price - 180000
                        if(remainingPropertyPrice < 180000):
                            stampDuty += 0.02*remainingPropertyPrice
                        else:
                            stampDuty += 0.02*180000
                            remainingPropertyPrice -= 180000
                            if (remainingPropertyPrice < 640000):
                                stampDuty += 0.03 * remainingPropertyPrice
                            else:
                                stampDuty += 0.03 * 640000
                                remainingPropertyPrice -= 640000
                                stampDuty += 0.04 * remainingPropertyPrice
                    lumpSumPayment = downPayment + optionFee + stampDuty

                    dictionary['buyerStampDuties'] = stampDuty

                    dictionary['lumpSumPayment'] = downPayment + \
                        optionFee + stampDuty

                    suggestedProperties.append(dictionary)

                    # Round values
                    for key, value in housingCalculate.items():
                        if (key != 'loanPeriod'):
                            housingCalculate[key] = round(value, 1)

                return render(request, "house/costBreakdown.html", {'mostAffordable': suggestedProperties[0], 'maxAffordable': suggestedProperties[1], 'housingCalculate': housingCalculate, 'username': username, "firstTime": firstTime})
        except:
            return redirect("/house/form/")

    else:
        return redirect('home')
