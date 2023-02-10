from django.db.models.fields import NullBooleanField
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
import json

from Finance.FinanceMgr import FinanceMgr
from .models import Asset, Debt, Information, OtherIncomeSource
from Main.AccountMgr import AccountMgr
from datetime import date, datetime
from Finance.models import *

from django.db import IntegrityError

# Create your views here.


def financeHome_view(request):
    if request.session.has_key('username'):
        username = request.session['username']

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        return render(request, 'finance/financeHome.html', {"username": username, "firstTime": firstTime})
    else:
        return render(request, 'home.html')


def updateUserInfo_View(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.user.get(username=username)
        financemanager = FinanceMgr(user)

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        if Information.objects.filter(user=username).exists():
            if (request.method == 'POST'):
                stringDate = request.POST.get("DoB")
                objDate = datetime.strptime(stringDate, '%Y-%m-%d').date()
                info = Information(DOB=objDate,
                                gender=request.POST.get("gender"),
                                education=request.POST.get("eLevel"),
                                maritalStatus=request.POST.get("mStatus"),
                                occupation=request.POST.get("Occupation"),
                                monthlyIncome=request.POST.get("mIncome"),
                                spouseMonthlyIncome=request.POST.get("sIncome"),
                                noOfDependents=request.POST.get(
                                    "noOfDependent"),
                                OAAmount=request.POST.get("OAcpf"),
                                SAAmount=request.POST.get("SAcpf"),
                                medisave=request.POST.get("MAcpf"))
                try:
                    financemanager.createInformation(info)
                except IntegrityError as error:
                    return render(request, "finance/updateError.html", {'username': username})

                financemanager.createInformation(info)

                print("Update Success")
                return redirect('/finance/financeHome/')
            else:
                userInfo = user.information
                print("DEBUGGING")
                print(userInfo.DOB)

                return render(request, 'finance/updateUserInfo.html',
                            {"username": username,
                            "firstTime": firstTime,
                            'DOB': userInfo.DOB.strftime('%Y-%m-%d'),
                            'gender': userInfo.gender,
                            'education': userInfo.education,
                            'maritalStatus': userInfo.maritalStatus,
                            'occupation': userInfo.occupation,
                            'monthlyIncome': userInfo.monthlyIncome,
                            'spouseMonthlyIncome': userInfo.spouseMonthlyIncome,
                            'noOfDependents': userInfo.noOfDependents,
                            'OAAmount': userInfo.OAAmount,
                            'SAAmount': userInfo.SAAmount,
                            'medisave': userInfo.medisave
                            })
        else:
            return redirect('/finance/questionaire/', {"username": username, "firstTime": firstTime})
    else:
        return render(request, 'home.html')


def formError_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'finance/formError.html', {"username": username})
    else:
        return render(request, 'home.html')


def updateError_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'finance/updateError.html', {"username": username})
    else:
        return render(request, 'home.html')


def questionaire_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.user.get(username=username)
        financemanager = FinanceMgr(user)

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        """
        #temp user for testing
        testuser = User.user.validate("swaggydaddy","swaggymcpants1")
        testuser = testuser[0]
        financemanager = FinanceMgr(testuser)
        """
        if (request.method == 'POST'):
            # Don't let them re-submit if they have the info obj already
            if Information.objects.filter(user=username).exists():
                return redirect('/finance/financeHome/')
            else:
                stringDate = request.POST.get("DoB")
                objDate = datetime.strptime(stringDate, '%Y-%m-%d').date()
                print("--DEBUGGING--")
                print(objDate)
                info = Information(DOB=objDate,
                                   gender=request.POST.get("gender"),
                                   education=request.POST.get("eLevel"),
                                   maritalStatus=request.POST.get("mStatus"),
                                   occupation=request.POST.get("Occupation"),
                                   monthlyIncome=request.POST.get("mIncome"),
                                   spouseMonthlyIncome=request.POST.get(
                                       "sIncome"),
                                   noOfDependents=request.POST.get(
                                       "noOfDependent"),
                                   OAAmount=request.POST.get("OAcpf"),
                                   SAAmount=request.POST.get("SAcpf"),
                                   medisave=request.POST.get("MAcpf"))

                try:
                    financemanager.createInformation(info)
                except IntegrityError as error:
                    return render(request, "finance/formError.html", {'username': username})

                financemanager.createInformation(info)
                print("DEBUG: printing DOB- ")
                print(user.information.DOB)

                # table data
                # for otherIncome
                oIncome_list = request.POST.getlist('oIncome[]')
                oAmount_list = request.POST.getlist('oAmount[]')

                print(oIncome_list)
                print(oAmount_list)

                for i in range(0, len(oIncome_list), 1):
                    financemanager.createIncomeSource(incomeSource=oIncome_list[i],
                                                      amount=oAmount_list[i])

                # for expense
                expense_list = request.POST.getlist('expense[]')
                eAmount_list = request.POST.getlist('eAmount[]')

                print(expense_list)
                print(eAmount_list)

                for i in range(0, len(expense_list), 1):
                    financemanager.createExpense(expenseName=expense_list[i],
                                                 amount=eAmount_list[i])

                # for asset
                asset_list = request.POST.getlist('asset[]')
                aValue_list = request.POST.getlist('aValue[]')
                aReturn_list = request.POST.getlist('aReturn[]')

                print(asset_list)
                print(aValue_list)
                print(aReturn_list)

                for i in range(0, len(asset_list), 1):
                    financemanager.createAsset(assetName=asset_list[i],
                                               amount=aValue_list[i],
                                               returns=aReturn_list[i])

                # for debt
                debt_list = request.POST.getlist('debt[]')
                totalDebt_list = request.POST.getlist('totalDebt[]')
                paidDebt_list = request.POST.getlist('paidDebt[]')
                debtInterest_list = request.POST.getlist('debtInterest[]')

                print(debt_list)
                print(totalDebt_list)
                print(paidDebt_list)
                print(debtInterest_list)

                for i in range(0, len(debt_list), 1):
                    financemanager.createDebt(debtName=debt_list[i],
                                              amount=totalDebt_list[i],
                                              repayment=paidDebt_list[i],
                                              interest=debtInterest_list[i])

                print("Created Successfully")
                return redirect('/finance/financeHome/')
        else:
            return render(request, 'finance/questionaire.html', {"username": username, "firstTime": firstTime})
    else:
        return render(request, 'home.html')


def balanceSheet_Result_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.user.get(username=username)
        financemanager = FinanceMgr(user)

        """
        #temp user for testing
        testuser = User.user.validate("swaggydaddy","swaggymcpants1")
        testuser = testuser[0]
        financemanager = FinanceMgr(testuser)
        """
        netWorth = 0
        totalAsset = 0
        totalDebt = 0

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        # Testing if the information object has been made. If not, need user to fill up questionaire
        if Information.objects.filter(user=username).exists():
            (asset_list, debt_list, netWorth, totalAsset,
             totalDebt) = financemanager.retrieveBalanceSheet()
            return render(request, 'finance/balanceSheet_Result.html',  {
                'asset_list': asset_list,
                'debt_list': debt_list,
                'networth': netWorth,
                'totalAsset': totalAsset,
                'totalDebt': totalDebt,
                'username': username
            })
        else:
            return redirect('/finance/questionaire/', {"username": username, "firstTime": firstTime})

    else:
        return render(request, 'home.html')


def balanceSheet_Edit_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.user.get(username=username)
        financemanager = FinanceMgr(user)

        """
        #temp user for testing
        testuser = User.user.validate("swaggydaddy","swaggymcpants1")
        testuser = testuser[0]
        financemanager = FinanceMgr(testuser)
        """
        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        if (request.method == 'POST'):
            asset_list = request.POST.getlist('asset[]')
            aValue_list = request.POST.getlist('aValue[]')
            aReturn_list = request.POST.getlist('aReturn[]')
            assetID_list = request.POST.getlist('assetID[]')
            deleteAsset_list = request.POST.getlist('deleteAsset[]')

            debt_list = request.POST.getlist('debt[]')
            totalDebt_list = request.POST.getlist('totalDebt[]')
            paidDebt_list = request.POST.getlist('paidDebt[]')
            debtInterest_list = request.POST.getlist('debtInterest[]')
            debtID_list = request.POST.getlist('debtID[]')
            deleteDebt_list = request.POST.getlist('deleteDebt[]')

            # Insert new records
            print(assetID_list)
            print(deleteAsset_list)

            for i in range(0, len(assetID_list), 1):
                if (assetID_list[i] == "-1"):
                    financemanager.createAsset(assetName=asset_list[i],
                                               amount=aValue_list[i],
                                               returns=aReturn_list[i])

            for i in range(0, len(debtID_list), 1):
                if (debtID_list[i] == "-1"):
                    financemanager.createDebt(debtName=debt_list[i],
                                              amount=totalDebt_list[i],
                                              repayment=paidDebt_list[i],
                                              interest=debtInterest_list[i])

            # Update the existing records with new records
            for i in range(0, len(asset_list), 1):
                if (assetID_list[i] != -1):
                    financemanager.updateAsset(index=assetID_list[i],
                                               assetName=asset_list[i],
                                               amount=aValue_list[i],
                                               returns=aReturn_list[i])

            for i in range(0, len(debt_list), 1):
                if (debtID_list[i] != -1):
                    financemanager.updateDebt(index = debtID_list[i],
                                        debtName = debt_list[i],
                                        amount = totalDebt_list[i],
                                        repayment = paidDebt_list[i],
                                        interest = debtInterest_list[i])

            #Delete the selected records
            #print("DEBUGGING: Testing deleteAsset_list")
            # print(deleteAsset_list)
            for i in range(0, len(deleteAsset_list), 1):
                if (deleteAsset_list[i] != "no"):  # assume no delete for new rows
                    print("DEBUG: deleting index: "+deleteAsset_list[i])
                    financemanager.deleteAsset(deleteAsset_list[i])
                    #print("Asset Successfully deleted")

            #print("DEBUGGING: Testing deleteDebt_list")
            # print(deleteDebt_list)
            for i in range(0, len(deleteDebt_list), 1):
                if (deleteDebt_list[i] != "no"):
                    #print("DEBUG: deleting index: "+deleteDebt_list[i])
                    financemanager.deleteDebt(deleteDebt_list[i])
                    #print("Debt Successfully deleted")

            return redirect('/finance/balanceSheet_Result/')

        else:
            (asset_list, debt_list, netWorth, totalAsset,
             totalDebt) = financemanager.retrieveBalanceSheet()

            return render(request, 'finance/balanceSheet_Edit.html',  {
                'asset_list': asset_list,
                'debt_list': debt_list,
                'networth': netWorth,
                'totalAsset': totalAsset,
                'totalDebt': totalDebt,
                'username': username,
                "firstTime": firstTime
            })

    else:
        return render(request, 'home.html')


def cashFlow_Result_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.user.get(username=username)
        financemanager = FinanceMgr(user)

        """
        #temp user for testing
        testuser = User.user.validate("swaggydaddy","swaggymcpants1")
        testuser = testuser[0]
        financemanager = FinanceMgr(testuser)
        """

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        monthlyIncome = 0
        spouseMonthlyIncome = 0
        netIncome = 0

        # Testing if the information object has been made. If not, need user to fill up questionaire
        if Information.objects.filter(user=username).exists():
            (monthlyIncome, spouseMonthlyIncome, oIncome_list, mExpense_list,
             netIncome) = financemanager.retrieveFinancialInformation()
            return render(request, 'finance/cashFlow_Result.html', {
                'oIncome_list': oIncome_list,
                'mExpense_list': mExpense_list,
                'monthlyIncome': monthlyIncome,
                'spouseMonthlyIncome': spouseMonthlyIncome,
                'netIncome': netIncome,
                'username': username
            })
        else:
            return redirect('/finance/questionaire/', {"firstTime": firstTime})

    else:
        return render(request, 'home.html')


def cashFlow_Edit_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.user.get(username=username)
        financemanager = FinanceMgr(user)
        """
        #temp user for testing
        testuser = User.user.validate("swaggydaddy","swaggymcpants1")
        testuser = testuser[0]
        financemanager = FinanceMgr(testuser)
        """

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        monthlyIncome = 0
        spouseMonthlyIncome = 0
        netIncome = 0

        if (request.method == 'POST'):
            oIncome_list = request.POST.getlist('oIncome[]')
            oAmount_list = request.POST.getlist('oAmount[]')
            oIncomeID_list = request.POST.getlist('oIncomeID[]')
            deleteIncome_list = request.POST.getlist('deleteIncome[]')

            expense_list = request.POST.getlist('expense[]')
            eAmount_list = request.POST.getlist('eAmount[]')
            expenseID_list = request.POST.getlist('expenseID[]')
            deleteExpense_list = request.POST.getlist('deleteExpense[]')

            monthlyIncome = request.POST.get('mIncomeAmount')
            spouseMonthlyIncome = request.POST.get('smIncomeAmount')

            # Insert new records
            # print(oIncomeID_list)
            for i in range(0, len(oIncomeID_list), 1):
                if (oIncomeID_list[i] == "-1"):
                    financemanager.createIncomeSource(incomeSource=oIncome_list[i],
                                                      amount=oAmount_list[i])

            # print(expenseID_list)
            for i in range(0, len(expenseID_list), 1):
                if (expenseID_list[i] == "-1"):
                    financemanager.createExpense(expenseName=expense_list[i],
                                                 amount=eAmount_list[i])

            # Update the existing records with new records

            print("DEBUGGING: UpdateIncomeSource")
            print(oIncomeID_list)
            print(oIncome_list)
            print(oAmount_list)

            for i in range(0, len(oIncome_list), 1):
                if (oIncomeID_list[i] != -1):
                    financemanager.updateIncomeSource(index=oIncomeID_list[i],
                                                      incomeSourceName=oIncome_list[i],
                                                      amount=oAmount_list[i])

            for i in range(0, len(expense_list), 1):
                if (expenseID_list[i] != -1):
                    financemanager.updateExpense(index=expenseID_list[i],
                                                 expenseName=expense_list[i],
                                                 amount=eAmount_list[i])

            # Delete the useless records
            # print("DEBUGGING")
            # print(deleteIncome_list)
            for i in range(0, len(deleteIncome_list), 1):
                if (deleteIncome_list[i] != "no"):
                    print("DEBUG: deleting index: " + deleteIncome_list[i])
                    financemanager.deleteIncomeSource(deleteIncome_list[i])
                    print("Income Successfully deleted")

            # print("DEBUGGING")
            # print(deleteExpense_list)
            for i in range(0, len(deleteExpense_list), 1):
                if (deleteExpense_list[i] != "no"):
                    print("DEBUG: deleting index: " + deleteExpense_list[i])
                    financemanager.deleteExpense(deleteExpense_list[i])
                    print("Expense Successfully deleted")

            return redirect('/finance/cashFlow_Result/')

        else:
            (monthlyIncome, spouseMonthlyIncome, oIncome_list, mExpense_list,
             netIncome) = financemanager.retrieveFinancialInformation()
            return render(request, 'finance/cashFlow_Edit.html', {
                'oIncome_list': oIncome_list,
                'mExpense_list': mExpense_list,
                'monthlyIncome': monthlyIncome,
                'spouseMonthlyIncome': spouseMonthlyIncome,
                'netIncome': netIncome,
                "username": username,
                "firstTime": firstTime,
            })

    else:
        return render(request, 'home.html')


def growWealth_view(request):
    if request.session.has_key('username'):

        # Testing if the information object has been made. If not, need user to fill up questionaire
        username = request.session['username']
        user = User.user.get(username=username)
        financeMgr = FinanceMgr(user)

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        if Information.objects.filter(user=username).exists():
            context = {"username": username}
            adviceList = financeMgr.retrieveAdvice()
            (cashFlowData, debtData, netWorthData) = financeMgr.projectFinance()
            cashFlowData = json.dumps(cashFlowData)
            debtData = json.dumps(debtData)
            netWorthData = json.dumps(netWorthData)
            context["adviceList"] = adviceList
            context["cashFlowData"] = cashFlowData
            context["debtData"] = debtData
            context["netWorthData"] = netWorthData
            return render(request, 'finance/growWealth.html', context)
        else:
            return redirect('/finance/questionaire/', {"username": username, "firstTime": firstTime})


    else:
        return redirect('login')