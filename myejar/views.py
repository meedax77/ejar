import datetime
from decimal import Decimal
from pyexpat import model
from django.forms import DecimalField
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Customers,Expenses, Payment_recived, Units, Buildings, Payment, Contracts, Login
from .forms import CustomerForm,CustomerSelectForm,ExpensesForm, BuildingSelectForm, RegisterForm, PaymentReciveForm, UnitForm, BuildingForm, ContractForm, PaymentForm, PaymentFormSet
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.db import models 
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.conf import settings
from datetime import date
from twilio.rest import Client



# Create your views here.

# urls
@login_required(login_url="login")
def dashboared(request):
    payments = Payment.objects.filter(amount__gt=0, payment_due__lt=datetime.date.today())
    # Number of active contracts
    active_contracts = Contracts.objects.filter(endDate__gte=datetime.date.today()).count()

    # Sum of payment amounts where the due date has passed
    total_due_amount = Payment.objects.filter(payment_due__lte=datetime.date.today()).aggregate(total_due=models.Sum('amount'))['total_due']

    # Count of payments where the due date has passed
    due_payments_count = Payment.objects.filter(payment_due__lte=datetime.date.today()).count()

    context = {
        'unitsModule': Units.objects.all(),
        'buildingsModule': Buildings.objects.all(),
        'customersModule': Customers.objects.all(),
        'contractModule': Contracts.objects.all(),
        'PaymentModule': payments,
        'contractModulecount': Contracts.objects.all().count(),
        'active_contracts': active_contracts,
        'total_due_amount': total_due_amount or 0,
        'due_payments_count': due_payments_count,
    }

    return render(request, 'dashboared.html', context)
    

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = Login(username = username, password = password)
        if data.is_valid():
            data.save()

    return render(request, 'login.html', {})

@login_required(login_url="login")
def customers(request):
    return render(request, 'customers.html',{'customersModule' : Customers.objects.all()})

@login_required(login_url="login")
def buildings(request):
    return render(request, 'buildings.html',{'buildingsModule' : Buildings.objects.all()})

@login_required(login_url="login")
def units(request):
    return render(request, 'units.html',{'unitsModule' : Units.objects.all()})

@login_required(login_url="login")
def contracts(request):
    return render(request, 'contracts.html',{'contractModule' : Contracts.objects.all()})

@login_required(login_url="login")
def settings(request):
    users = User.objects.all()  # Retrieve all users
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
    else:
        form = RegisterForm()

    return render(request, 'settings.html', {"form": form, "users": users})

def docs(request):
    return render(request, 'docs.html')



#post functions------------------------------------------------
@login_required(login_url="login")
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')  # Replace 'customer_list' with the URL name of the customer list view
    else:
        form = CustomerForm()
    
    return render(request, 'add_customer.html', {'form': form})

#------------------------
@login_required(login_url="login")
def add_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('buildings')  # Replace 'customer_list' with the URL name of the customer list view
    else:
        form = BuildingForm()
    
    return render(request, 'add_building.html', {'form': form})

#------------------------------
@login_required(login_url="login")
def add_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('units')  # Replace 'customer_list' with the URL name of the customer list view
    else:
        form = UnitForm()
    
    return render(request, 'add_unit.html', {'form': form})

#-----------------------------------

@login_required(login_url="login")
def ContractCreate(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contracts')  # Replace 'customer_list' with the URL name of the customer list view
    else:
        form = ContractForm()
    
    return render(request, 'contract_create_or_update.html', {'form': form})

#---------------------------------
@login_required(login_url="login")
def create_payment(request, contract_id):
    contract = get_object_or_404(Contracts, id=contract_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.contract = contract
            payment.save()
            return redirect('contract_detail', contract_id=contract_id)  # Update the redirection with contract_id
    else:
        form = PaymentForm()
    
    context = {
        'contract': contract,
        'form': form,
    }
    return render(request, 'create_payment.html', context)

#delete functions ------------------------------------
@login_required(login_url="login")
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customers, cID=customer_id)
    
    # Check if the customer is related to any contracts
    if Contracts.objects.filter(customer=customer).exists():
        # Customer is related to a contract, prevent deletion and display error message
        messages.error(request, "المستأجر مرتبط بعقد ايجار ولن يتم حذفه حتى يتم حذف العقد")
        return redirect('customers')  # Replace 'customers' with the URL name of the customer list view
    
    # Perform any additional logic here if needed
    
    customer.delete()
    
    return redirect('customers')  # Replace 'customers' with the URL name of the customer list view

#-----------------------------------------
@login_required(login_url="login")
def delete_building(request, building_id):
    building = get_object_or_404(Buildings, dID=building_id)
    
    if Units.objects.filter(building=building).exists():
        messages.error(request, "المبنى مرتبط بوحدات  ولن يتم حذفه حتى يتم حذف الوحدات")
        return redirect('buildings') 
    
    
    building.delete()
    return redirect('buildings')  # Replace 'customers' with the URL name of the customer list view

#-------------------------------------------
@login_required(login_url="login")
def delete_unit(request, unit_id):
    unit = get_object_or_404(Units, uNumber=unit_id)
    
    if Contracts.objects.filter(unit=unit).exists():
        messages.error(request, "الوحدة مرتبطة بعقد ايجار ولن يتم حذفها حتى يتم حذف العقد")
        return redirect('units') 
    
    
    unit.delete()
    return redirect('units')  


#----------------------------------
@login_required(login_url="login")
def delete_contract(request, contract_id):
    contract = get_object_or_404(Contracts, contractNumber=contract_id)
    contract.delete()
    return redirect('contracts')  
#----------------------------------
@login_required(login_url="login")
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    if Payment_recived.objects.filter(payment=payment).exists():
        messages.error(request, "يوجد سندات قبض بالدفعة المحددة يرجى حذف السندات لحذف الدفعة ")
        return redirect('contract_detail', contract_id=payment.contract.id) 
    
    
    payment.delete()
    return redirect('contract_detail', contract_id=payment.contract.id)

#------------------------------------
@login_required(login_url="login")
def delete_payment_received(request, received_payment_id):
    received_payment = get_object_or_404(Payment_recived, id=received_payment_id)
    received_payment.delete()
    return redirect('contract_detail', contract_id=received_payment.payment.contract.id)
#edit functions ------------------------------------
@login_required(login_url="login")
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customers, cID=customer_id)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')  # Replace 'customers' with the URL name of the customer list view
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'add_customer.html', {'form': form, 'customer': customer})

#-------------------------------------------------------
@login_required(login_url="login")
def edit_building(request, building_id):
    building = get_object_or_404(Buildings, dID=building_id)
    
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES, instance=building)
        if form.is_valid():
            form.save()
            return redirect('buildings')  # Replace 'customers' with the URL name of the customer list view
    else:
        form = BuildingForm(instance=building)
    
    return render(request, 'add_building.html', {'form': form, 'buildings': building})

#--------------------------------------------------------
@login_required(login_url="login")
def edit_unit(request, unit_id):
    unit = get_object_or_404(Units, uNumber=unit_id)
    
    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('units')  # Replace 'customers' with the URL name of the customer list view
    else:
        form = UnitForm(instance=unit)
    
    return render(request, 'add_unit.html', {'form': form, 'unit': unit})


#---------------------------------------------------------
#contract detail page
@login_required(login_url="login")
def contract_detail(request, contract_id):
    contract = get_object_or_404(Contracts, id=contract_id)
    context = {
        'contract': contract,
        'Payment_recivedModule' : Payment_recived.objects.all()
    }
    return render(request, 'contract_detail.html', context)
#----------------------------------------------------------
from decimal import Decimal
@login_required(login_url="login")
def payment_received(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == 'POST':
        form = PaymentReciveForm(request.POST)
        if form.is_valid():
            payment_received = form.save(commit=False)
            payment_received.payment = payment
            payment_received.save()

            # Subtract the received amount from the payment's amount
            payment.amount -= payment_received.received_amount
            payment.save()

            return redirect('contract_detail', contract_id=payment.contract.id)
    else:
        form = PaymentReciveForm()

    context = {
        'form': form,
        'payment': payment,
    }
    return render(request, 'payment_received.html', context)

#-------------------------------------------------------

from django.db.models import Sum
@login_required(login_url="login")
def print_payment_received(request, received_payment_id):
    received_payment = get_object_or_404(Payment_recived, id=received_payment_id)

    # Get the related contract
    contract = received_payment.payment.contract

    # Calculate the total received amount for the contract
    total_received_amount = Payment_recived.objects.filter(payment__contract=contract).aggregate(Sum('received_amount')).get('received_amount__sum')

    context = {
        'received_payment': received_payment,
        'total_received_amount': total_received_amount,
    }
    return render(request, 'print_payment_received.html', context)



#---------------------------------------------------------
from django.db.models import Sum

@login_required(login_url="login")
def generate_report(request):
    if request.method == 'POST':
        form = CustomerSelectForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            
            # Retrieve contracts related to the selected customer
            contracts = Contracts.objects.filter(customer=customer)
            
            # Calculate the sum of received_amount of all contracts
            total_received_amount = Payment_recived.objects.filter(payment__contract__in=contracts).aggregate(total_received_amount=Sum('received_amount'))['total_received_amount']
            
            # Calculate the sum of payment amount of all contracts
            total_payment_amount = Payment.objects.filter(contract__in=contracts).aggregate(total_payment_amount=Sum('amount'))['total_payment_amount']
            
            context = {
                'customer': customer,
                'contracts': contracts,
                'total_received_amount': total_received_amount,
                'total_payment_amount': total_payment_amount,
            }
            
            return render(request, 'report.html', context)
    else:
        form = CustomerSelectForm()
    
    return render(request, 'select_customer.html', {'form': form})


#----------------------------------


@login_required(login_url="login")
def generate_building_report(request):
    if request.method == 'POST':
        form = BuildingSelectForm(request.POST)
        if form.is_valid():
            building = form.cleaned_data['building']
            
            # Retrieve all units related to the selected building
            units = Units.objects.filter(building=building)
            
            # Retrieve contracts related to the selected building
            contracts = Contracts.objects.filter(unit__in=units)
            expenses = Expenses.objects.filter(eBuilding=building)
            # Calculate the sum of eamount
            expenses_total = sum(expense.eamount for expense in expenses)

            # Calculate the sum of total_amount
            contracts_total = sum(contract.total_amount for contract in contracts)
            
            context = {
                'building': building,
                'units': units,
                'contracts': contracts,
                'expenses' : expenses,
                'expenses_total': expenses_total,
                'contracts_total': contracts_total,
            }
            
            return render(request, 'building_report.html', context)
    else:
        form = BuildingSelectForm()
    
    return render(request, 'select_building.html', {'form': form})


#--------------------------------------
from django.db.models import Count, OuterRef, Subquery


@login_required(login_url="login")
def customers_report(request):
    payment_subquery = Payment.objects.filter(
        contract__customer=OuterRef('pk'),
        amount__gt=0
    ).values('contract__customer').annotate(payment_count=Count('pk')).values('payment_count')

    customers = Customers.objects.annotate(
        contract_count=Count('contracts'),
        payment_count=Subquery(payment_subquery)
    )

    return render(request, 'customers_report.html', {'customers': customers})



#---------------------------------------
from datetime import date

@login_required(login_url="login")
def contract_report(request):
    filter_date = request.GET.get('filter_date')
    filter_contract_kind = request.GET.get('filter_contract_kind')

    contracts = Contracts.objects.all()

    if filter_date:
        contracts = contracts.filter(startDate__lte=filter_date, endDate__gte=filter_date)

    if filter_contract_kind:
        contracts = contracts.filter(contract_kind=filter_contract_kind)

    today = date.today()
    active_contracts_count = contracts.filter(startDate__lte=today, endDate__gte=today).count()
    upcoming_contracts_count = contracts.filter(startDate__gt=today).count()
    overdue_contracts_count = contracts.filter(endDate__lt=today).count()

    return render(request, 'contract_report.html', {
        'contracts': contracts,
        'active_contracts_count': active_contracts_count,
        'upcoming_contracts_count': upcoming_contracts_count,
        'overdue_contracts_count': overdue_contracts_count,
    })


#--------------------------------------------
from django.db.models import Q

@login_required(login_url="login")
def buildings_report(request):
    filter_b_kind = request.GET.get('filter_b_kind')
    buildings = Buildings.objects.all()
    buildings = Buildings.objects.annotate(unit_count=Count('units'))

    count_commercial = buildings.filter(bKind="تجاري").count()
    count_residential = buildings.filter(bKind="سكني").count()
    count_mixed = buildings.filter(bKind="سكني وتجاري").count()

    if filter_b_kind:
        buildings = buildings.filter(bKind=filter_b_kind)

    return render(request, 'buildings_report.html', {
        'buildings': buildings,
        'count_commercial': count_commercial,
        'count_residential': count_residential,
        'count_mixed': count_mixed,
    })


#--------------------------------------

@login_required(login_url="login")
def payment_report(request):
    filter_start_date = request.GET.get('filter_start_date')
    filter_end_date = request.GET.get('filter_end_date')

    payments = Payment_recived.objects.all().select_related('payment__contract', 'payment__contract__customer')

    if filter_start_date and filter_end_date:
        payments = payments.filter(received_date__range=[filter_start_date, filter_end_date])

    payments = payments.order_by('-received_date')

    # Calculate the required sums
    residential_revenue = payments.filter(payment__contract__contract_kind='سكني').aggregate(Sum('received_amount'))['received_amount__sum']
    commercial_payments = payments.filter(payment__contract__contract_kind='تجاري')
    commercial_revenue = commercial_payments.aggregate(Sum('received_amount'))['received_amount__sum']
    total_commercial_revenue = 0
    total_revenue = payments.aggregate(Sum('received_amount'))['received_amount__sum']

    vat_revenue = commercial_payments.aggregate(Sum('received_amount'))['received_amount__sum']
    if vat_revenue is not None:
        vat_revenue = vat_revenue * Decimal('0.15')

    if commercial_revenue is not None:
        commercial_revenue = commercial_revenue * Decimal('0.85')

    for payment in commercial_payments:
        total_commercial_revenue = commercial_revenue + (vat_revenue or Decimal('0'))

    return render(request, 'payment_report.html', {
        'payments': payments,
        'filter_start_date': filter_start_date,
        'filter_end_date': filter_end_date,
        'residential_revenue': residential_revenue,
        'commercial_revenue': commercial_revenue,
        'vat_revenue': vat_revenue,
        'total_commercial_revenue': total_commercial_revenue,
        'total_revenue': total_revenue,
    })


#--------------------------------
from django.db.models import F, DecimalField, FloatField
from django.db.models.functions import Cast

@login_required(login_url="login")
def vat_report(request):
    filter_start_date = request.GET.get('filter_start_date')
    filter_end_date = request.GET.get('filter_end_date')

    payments = Payment_recived.objects.filter(payment__contract__contract_kind='تجاري')

    if filter_start_date and filter_end_date:
        payments = payments.filter(received_date__range=[filter_start_date, filter_end_date])

    payments = payments.annotate(
        vat=Cast(F('received_amount') * 0.15, output_field=DecimalField()),
        amount_without_vat=Cast(F('received_amount') * 0.85, output_field=DecimalField()),
    ).order_by('-received_date')

    payment_amount_without_vat_sum = payments.aggregate(Sum('amount_without_vat'))['amount_without_vat__sum']
    vat_sum = payments.aggregate(Sum('vat'))['vat__sum']
    total_commercial_revenue_sum = payments.aggregate(Sum('received_amount'))['received_amount__sum']

    return render(request, 'vat_report.html', {
        'payments': payments,
        'filter_start_date': filter_start_date,
        'filter_end_date': filter_end_date,
        'payment_amount_without_vat_sum': payment_amount_without_vat_sum,
        'vat_sum': vat_sum,
        'total_commercial_revenue_sum': total_commercial_revenue_sum,
    })


#--------------------------------------------
@login_required(login_url="login")
def expenses(request):
    return render(request, 'expenses.html',{'expensesModule' : Expenses.objects.all()})

#--------------------------------------------

@login_required(login_url="login")
def add_expenses(request):
    if request.method == 'POST':
        form = ExpensesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('expenses')  # Replace 'customer_list' with the URL name of the customer list view
    else:
        form = ExpensesForm()
    
    return render(request, 'add_expenses.html', {'form': form})


#----------------------------------------------
@login_required(login_url="login")
def delete_expenses(request, expenses_id):
    expenses = get_object_or_404(Expenses, id=expenses_id)
    
    # Check if the customer is related to any contracts

    expenses.delete()
    
    return redirect('expenses')  

#-------------------------------------------------
@login_required(login_url="login")
def print_expenses(request, expenses_id):
    expenses = get_object_or_404(Expenses, id=expenses_id)

    # Get the related contract

    # Calculate the total received amount for the contract

    context = {
        'expenses': expenses,
    }
    return render(request, 'print_expenses.html', context)