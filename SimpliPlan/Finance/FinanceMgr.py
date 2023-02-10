from .models import *
from datetime import date
from Main.AccountMgr import *

INCOME_STRING = f"Your main income is in the %d-%d quartile."
EXPENDITURE_STRING = f"Your expenditure is %.2f%% %s than the average in your income quartile."
EXPENDITURE_STRING2 = f"Your expenditure is around the same as the average for your income quartile"
DEBT_HIGH_STRING = f"Your debt repayment per month is too high, consider refinancing some of your debts"
DEBT_INTEREST_STRING = f"You have a Debt (%s) which have a very high interest rate of %.2f. Consider refinancing or clearing this debt first"
NO_DEBT_STRING = f"You have no debt"
CASH_FLOW_STRING = f"You have a negative cashflow"


class FinanceMgr:
    def __init__(self, user):
        self.user = user

    def retrieveAdvice(self):
        adviceList = list()
        (assetList, debtList, netWorth, totalAsset,
         totalDebt) = self.retrieveBalanceSheet()
        (monthlyIncome, spouseMonthlyIncome, incomeList, expenseList,
         netIncome) = self.retrieveFinancialInformation()
        totalExpense = 0
        for expense in expenseList:
            totalExpense += expense.amount
        for incomeInfo in IncomeQuartile.objects.all():
            if monthlyIncome < incomeInfo.averageIncome or incomeInfo.quartile == 90:
                adviceList.append(
                    (INCOME_STRING % (incomeInfo.quartile-10, incomeInfo.quartile+10), 0))
                difference = (totalExpense-incomeInfo.averageExpenditure) / \
                    incomeInfo.averageExpenditure
                if abs(difference) > 0.1:
                    if difference > 0:
                        adviceList.append((EXPENDITURE_STRING %
                                          (difference*100, "higher"), -1))
                    else:
                        adviceList.append((EXPENDITURE_STRING %
                                          (-difference*100, "lower"), 1))
                else:
                    adviceList.append((EXPENDITURE_STRING2, 0))
                break

        totalRepayment = 0
        cashFlow = self.calculateCashFlow()
        for debt in debtList:
            if debt.interest > 0.04:
                adviceList.append((DEBT_INTEREST_STRING %
                                  (debt.debtName, debt.interest), -1))
            totalRepayment += debt.repayment

        totalIncome = monthlyIncome
        for income in incomeList:
            totalIncome += income.amount
        if totalRepayment/totalIncome >= 0.6:
            adviceList.append((DEBT_HIGH_STRING, -1))
        if totalDebt == 0:
            adviceList.append((NO_DEBT_STRING, 1))

        if cashFlow < 0:
            adviceList.append((CASH_FLOW_STRING, -1))
        return adviceList

    def retrieveBalanceSheet(self):
        self.asset = Asset.objects.filter(information=self.user.information)
        self.debt = Debt.objects.filter(information=self.user.information)
        netWorth = 0
        totalAsset = 0
        totalDebt = 0
        # print("Assets")
        for a in self.asset:
            totalAsset += a.amount
            #print("%s %f %f"%(a.assetName, a.amount, a.returns))

        # print("Debt")
        for d in self.debt:
            totalDebt += d.amount
            #print("%s %f %f"%(d.debtName, d.amount, d.repayment))
        netWorth = totalAsset - totalDebt
        return (self.asset, self.debt, netWorth, totalAsset, totalDebt)

    def retrieveFinancialInformation(self):
        self.incomeSource = OtherIncomeSource.objects.filter(
            information=self.user.information)
        self.expense = MonthlyExpense.objects.filter(
            information=self.user.information)
        netIncome = 0
        # print("Income")
        for income in self.incomeSource:
            netIncome += income.amount
            #print("%s %f"%(income.incomeSource, income.amount))
        # print("Expenses")
        for expense in self.expense:
            netIncome -= expense.amount
            #print("%s %f"%(expense.expenseName, expense.amount))
        netIncome += self.user.information.monthlyIncome
        #netIncome += self.user.information.spouseMonthlyIncome
        #print("%s %f"%("monthlyIncome", self.user.information.monthlyIncome))
        #print("%s %f"%("spouseMonthlyIncome", self.user.information.spouseMonthlyIncome))
        return (self.user.information.monthlyIncome, self.user.information.spouseMonthlyIncome, self.incomeSource, self.expense, netIncome)

    def calculateCashFlow(self):
        (assetList, debtList, netWorth, _, _) = self.retrieveBalanceSheet()
        (monthlyIncome, spouseMonthlyIncome, incomeList, expenseList,
         netIncome) = self.retrieveFinancialInformation()
        cashFlow = netIncome
        # for asset in assetList:
        #cashFlow+=asset.amount * asset.returns
        for debt in debtList:
            cashFlow -= debt.repayment

        return cashFlow

    def projectFinance(self):
        (assetList, debtList, netWorth, _, _) = self.retrieveBalanceSheet()
        (monthlyIncome, spouseMonthlyIncome, incomeList, expenseList,
         netIncome) = self.retrieveFinancialInformation()
        cashFlowData = list()
        debtData = list()
        netWorthData = list()
        totalCashFlow = 0
        for i in range(0, 10):

            cashFlow = netIncome * 12
            totalDebt = 0
            totalAsset = 0
            for asset in assetList:
                asset.amount += asset.amount * asset.returns
                totalAsset += asset.amount

            for debt in debtList:
                totalDebt += debt.amount
                if debt.amount != 0:
                    if debt.amount < debt.repayment*12:
                        cashFlow -= debt.amount
                        debt.amount = 0
                    else:
                        cashFlow -= debt.repayment*12
                        debt.amount -= debt.repayment*12
                    debt.amount += debt.amount*debt.interest

            cashFlowData.append(cashFlow)
            debtData.append(totalDebt)
            netWorthData.append(totalAsset-totalDebt+totalCashFlow)
            totalCashFlow += cashFlow
            netIncome = netIncome * 1.02

        return (cashFlowData, debtData, netWorthData)

    def updateBalanceSheet(self):
        return True

    def updateFinancialInformation(self, actions):
        for action in actions:
            action()
        return True

    @staticmethod
    def loginAndDoStuff():
        user = AccountMgr.login("bob", "password")
        finMgr = FinanceMgr(user)

        return finMgr

    @staticmethod
    def helper(user):
        info = Information(user=user, DOB=date.today(), gender="male", education="diploma",
                           maritalStatus="Single", occupation="teacher", monthlyIncome=1000,
                           spouseMonthlyIncome=100, noOfDependents=1, OAAmount=100, SAAmount=100,
                           medisave=100)
        return info

    def createInformation(self, information):
        information.user = self.user
        information.save()
        return True

    def updateAsset(self, index, assetName, amount, returns):
        asset = Asset.objects.filter(
            information=self.user.information).filter(id=index)
        if len(asset) > 0:
            a = asset[0]
            a.assetName = assetName
            a.amount = amount
            a.returns = returns
            a.save()
            return True
        return False

    def createAsset(self, assetName, amount, returns):
        newAsset = Asset(information=self.user.information,
                         assetName=assetName, amount=amount, returns=returns)
        newAsset.save()
        return True

    def deleteAsset(self, index):
        asset = Asset.objects.filter(
            information=self.user.information).filter(id=index)
        if len(asset) > 0:
            asset[0].delete()
            return True
        return False

    def updateDebt(self, index, debtName, amount, repayment, interest):
        debt = Debt.objects.filter(
            information=self.user.information).filter(id=index)
        if len(debt) > 0:
            d = debt[0]
            d.debtName = debtName
            d.amount = amount
            d.repayment = repayment
            d.interest = interest
            d.save()
            return True
        return False

    def createDebt(self, debtName, amount, repayment, interest):
        newDebt = Debt(information=self.user.information, debtName=debtName,
                       amount=amount, repayment=repayment, interest=interest)
        newDebt.save()
        return True

    def deleteDebt(self, index):
        debt = Debt.objects.filter(
            information=self.user.information).filter(id=index)
        if len(debt) > 0:
            debt[0].delete()
            return True
        return False

    def updateIncomeSource(self, index, incomeSourceName, amount):
        incomeSource = OtherIncomeSource.objects.filter(
            information=self.user.information).filter(id=index)
        if len(incomeSource) > 0:
            i = incomeSource[0]
            i.incomeSource = incomeSourceName
            i.amount = amount
            i.save()
            return True
        return False

    def createIncomeSource(self, incomeSource, amount):
        newIncome = OtherIncomeSource(
            information=self.user.information, incomeSource=incomeSource, amount=amount)
        newIncome.save()
        return True

    def deleteIncomeSource(self, index):
        incomeSource = OtherIncomeSource.objects.filter(
            information=self.user.information).filter(id=index)
        if len(incomeSource) > 0:
            incomeSource[0].delete()
            return True
        return False

    def updateExpense(self, index, expenseName, amount):
        expense = MonthlyExpense.objects.filter(
            information=self.user.information).filter(id=index)
        if len(expense) > 0:
            e = expense[0]
            e.expenseName = expenseName
            e.amount = amount
            e.save()
            return True
        return False

    def createExpense(self, expenseName, amount):
        newExpense = MonthlyExpense(
            information=self.user.information, expenseName=expenseName, amount=amount)
        newExpense.save()
        return True

    def deleteExpense(self, index):
        expense = MonthlyExpense.objects.filter(
            information=self.user.information).filter(id=index)
        if len(expense) > 0:
            expense[0].delete()
            return True
        return False
