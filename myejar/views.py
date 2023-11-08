import datetime
from decimal import Decimal
from pyexpat import model
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Customers, Payment_recived, Units, Buildings, Payment, Contracts, Login
from .forms import CustomerForm,CustomerSelectForm, RegisterForm, PaymentReciveForm, UnitForm, BuildingForm, ContractForm, PaymentForm, PaymentFormSet
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
@login_required(login_url="login")
def generate_report(request):
    if request.method == 'POST':
        form = CustomerSelectForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            
            # Retrieve contracts related to the selected customer
            contracts = Contracts.objects.filter(customer=customer)
            
            # Retrieve payments related to the contracts
            payments = Payment.objects.filter(contract__in=contracts)
            
            # Retrieve received payments related to the payments
            received_payments = Payment_recived.objects.filter(payment__in=payments)
            
            context = {
                'customer': customer,
                'contracts': contracts,
                'payments': payments,
                'received_payments': received_payments,
            }
            
            return render(request, 'report.html', context)
    else:
        form = CustomerSelectForm()
    
    return render(request, 'select_customer.html', {'form': form})

#--------------------
import pywhatkit

def send_whatsapp_message(phone_number, message):
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_='whatsapp:' + settings.TWILIO_PHONE_NUMBER,
        to='whatsapp:' + phone_number
    )
    print('WhatsApp message sent:', message.sid)

def check_payment_due_date(request):
    due_date = date(2023, 11, 8)
    current_date = date.today()

    if current_date >= due_date:
        numbers = ['+966532256416', '+966530864596', '+966540843438']
        phone_number = numbers
        message = 'حلت الدفعة للعميل: ريان بمبلغ وقدره 500 ريال'
        send_whatsapp_message(phone_number, message)

    return HttpResponse('Payment due date checked.')


