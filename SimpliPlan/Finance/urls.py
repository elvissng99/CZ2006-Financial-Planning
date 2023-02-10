from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('questionaire/', views.questionaire_view, name="questionaire"),
    path('balanceSheet_Result/', views.balanceSheet_Result_view,name="balanceSheet_Result"),
    path('balanceSheet_Edit/', views.balanceSheet_Edit_view,name="balanceSheet_Edit"),
    path('cashFlow_Result/', views.cashFlow_Result_view, name="ccashFlow_Result"),
    path('cashFlow_Edit/', views.cashFlow_Edit_view, name="cashFlow_Edit"),
    path('financeHome/', views.financeHome_view, name="financeHome"),
    path('formError/', views.formError_view, name="formError"),
    path('growWealth/', views.growWealth_view, name="growWealth"),
    path('updateUserInfo/', views.updateUserInfo_View, name="updateUserInfo"),
    path('updateError/', views.updateError_view, name="updateError"),
]
