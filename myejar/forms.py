from django import forms
from .models import Customers, Payment_recived, Units, Contracts, Buildings , Payment
from decimal import Decimal
from django.forms import formset_factory, inlineformset_factory
from typing import Type
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
        widgets = {
            'cDob': forms.DateInput(attrs={'type': 'date'}),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = '__all__'


class PaymentReciveForm(forms.ModelForm):
    class Meta:
        model = Payment_recived
        fields = ['received_amount', 'received_date', 'payment_method','doc_number']
        widgets = {
                'received_date': forms.DateInput(attrs={'type': 'date'}),
            }
        



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount','payment_due']
        widgets = {
                'payment_due': forms.DateInput(attrs={'type': 'date'}),
            }
        
PaymentFormSet = inlineformset_factory(
    Contracts, Payment, form=PaymentForm,
    extra= 1 , can_delete= True, can_delete_extra= False
)




class ContractForm(forms.ModelForm):

    class Meta:
        model = Contracts
        fields = ['contract_kind','contractNumber', 'customer', 'unit', 'startDate', 'endDate', 'payment_amount']
        widgets = {
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
        }




class BuildingForm(forms.ModelForm):
    class Meta:
        model = Buildings
        fields = '__all__'



class CustomerSelectForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customers.objects.all(), label='  المستأجر')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name" ,"email", "password1", "password2"]


class BuildingSelectForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Buildings.objects.all(), label='  المبنى')