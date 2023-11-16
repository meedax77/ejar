from django.conf import settings
from django.urls import include, path
from . import views
from .views import  ContractCreate,generate_report, vat_report,  buildings_report, contract_report, customers_report,payment_received, create_payment, contract_detail,generate_building_report



urlpatterns = [
    path('', views.dashboared,  name = 'dashboared'),
    path('login', views.login, name = 'login'),
    path('customers', views.customers, name = 'customers'),
    path('buildings', views.buildings, name = 'buildings'),
    path('settings', views.settings, name = 'settings'),
    path('units', views.units, name = 'units'),
    path('contracts', views.contracts, name = 'contracts'),
    path('docs', views.docs, name = 'docs'),
    #----------------------------------------
    path('customers/add/', views.add_customer, name='add_customer'),
    path('delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    #----------------------------------------
    path('buildings/add/', views.add_building, name='add_building'),    path('delete/<int:building_id>/', views.delete_building, name='delete_building'),
    path('edit_building/<int:building_id>/', views.edit_building, name='edit_building'),
    path('delete_building/<int:building_id>/', views.delete_building, name='delete_building'),
    #----------------------------------------
    path('units/add/', views.add_unit, name='add_unit'),
    path('delete_unit/<int:unit_id>/', views.delete_unit, name='delete_unit'),
    path('edit_unit/<int:unit_id>/', views.edit_unit, name='edit_unit'),
    #----------------------------------------
    path('create/',views.ContractCreate, name='contract_create_or_update'),
    path('delete_contract/<int:contract_id>/', views.delete_contract, name='delete_contract'),
    #----------------------------------------
    path('contract/detail/<int:contract_id>/', views.contract_detail, name='contract_detail'),    #----------------------------------------
    path('create-payment/<int:contract_id>/', create_payment, name='create_payment'),   
    path('payment/received/<int:payment_id>/', payment_received, name='payment_received'), 
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('payment/received/<int:received_payment_id>/delete/', views.delete_payment_received, name='delete_payment_received'),
    path('payment/received/<int:received_payment_id>/print/', views.print_payment_received, name='print_payment_received'),
    #--------------------------------------------------
    path('report/', generate_report, name='generate_report'),
    path('generate_building_report/', generate_building_report, name='generate_building_report'),
    path('customers_report/', customers_report, name='customers_report'),
    path('contract-report/', contract_report, name='contract_report'),
    path('buildings-report/', buildings_report, name='buildings_report'),
    path('payment_report/', views.payment_report, name='payment_report'),
    path('vat-report/', vat_report, name='vat_report'),
    #------------------------------------
    path('', include('django.contrib.auth.urls')),
    #---------------------------------------
    path('expenses', views.expenses, name = 'expenses'),
    path('expenses/add/', views.add_expenses, name='add_expenses'),
    path('delete_expenses/<int:expenses_id>/', views.delete_expenses, name='delete_expenses'),
    path('expenses/done/<int:expenses_id>/print/', views.print_expenses, name='print_expenses'),


    ]







