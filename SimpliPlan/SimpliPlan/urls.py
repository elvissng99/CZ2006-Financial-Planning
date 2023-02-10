"""SimpliPlan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from Main.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    home_view,
    password_change_view,
    verify_username_view,
    password_reset_view,
    password_reset_confirm_view,
    password_reset_complete_view,
)

from Car.views import (
    search_view,
    results_view,
    details_view,
    trip_delete,
)

from Finance.views import (
    financeHome_view,
    questionaire_view,
    balanceSheet_Result_view,
    balanceSheet_Edit_view,
    cashFlow_Result_view,
    cashFlow_Edit_view,
    growWealth_view,
    formError_view,
    updateError_view,
    updateUserInfo_View,
)

from House.views import (
    form_view,
    costBreakdown_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('account/', account_view, name="account"),
    path('password_change/', password_change_view, name='password_change'),
    path('', home_view, name="home"), 

    # Car urls
    path('car/search/', search_view, name="car_search"),
    path('car/results/', results_view, name="car_results"),
    path('car/details/<int:pk>/', details_view, name="car_details"),
    path('car/details/<int:pk>/delete/', trip_delete, name="trip_delete"),

    # Password reset Urls
    path('password_reset_confirm/<username>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('verify_username/', verify_username_view, name='verify_username'),
    path('password_reset_complete/', password_reset_complete_view ,name='password_reset_complete'),

    # Path for house pages
    path('house/form/', form_view, name = 'form'),
    path('house/costBreakdown/', costBreakdown_view, name = 'costBreakdown'),

    # Path for finance pages
    path('finance/questionaire/', questionaire_view, name="questionaire"),
    path('finance/balanceSheet_Result/', balanceSheet_Result_view, name="balanceSheet_Result"),
    path('finance/balanceSheet_Edit/', balanceSheet_Edit_view, name="balanceSheet_Edit"),
    path('finance/cashFlow_Result/', cashFlow_Result_view, name="cashFlow_Result"),
    path('finance/cashFlow_Edit/', cashFlow_Edit_view, name="cashFlow_Edit"),
    path('finance/financeHome/', financeHome_view, name="financeHome"),
    path('finance/formError/', formError_view, name="formError"),
    path('finance/growWealth/', growWealth_view, name="growWealth"),
    path('finance/updateUserInfo/', updateUserInfo_View, name="updateUserInfo"),
    path('finance/updateError/', updateError_view, name="updateError"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
