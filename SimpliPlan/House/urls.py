from django.urls import include, path
from . import views

urlpatterns = [
    # path('houseInsertUserData', views.houseInsertUserData_view, name = 'houseInsertUserData'),
    # path('houseInsertHousingCalculate', views.houseInsertHousingCalculate_view, name = 'houseInsertHousingCalculate'),
    path('house/form/', views.form_view, name='form'),
    path('house/costBreakdown/', views.costBreakdown_view, name='costBreakdown'),
]
