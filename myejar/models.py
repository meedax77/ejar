from decimal import Decimal
from django.db import models
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save


from django.forms import ValidationError

#customers
from django.db import models

class Customers(models.Model):
    kind = [
        ("فرد", "فرد"),
        ("مؤسسة", "مؤسسة"),
    ]
    ckind = models.CharField(max_length=50, choices=kind, verbose_name="نوع المستأجر")
    cID = models.BigIntegerField(verbose_name="رقم الاثبات")
    cDob = models.DateField(verbose_name="تاريخ الميلاد")
    cName = models.CharField(max_length=50, verbose_name="اسم المستأجر")
    cNumber = models.BigIntegerField(max_length=10, verbose_name="رقم المستأجر")
    cIdImage = models.ImageField(upload_to='Idphotos/%y/%m/%d', blank=True, verbose_name="صورة الاثبات")

    def __str__(self):
        return self.cName

    class Meta:
        verbose_name = 'المستأجرين'




class Buildings (models.Model):
    kind = [
        ("سكني","سكني"),
        ("تجاري","تجاري"),
        ("سكني وتجاري","سكني وتجاري"),
    ]
    bKind = models.CharField(max_length=50, choices=kind, verbose_name="نوع المبنى")
    dName = models.CharField(max_length=50, verbose_name=" اسم العقار في الصك ", blank=True)
    dID = models.CharField(primary_key=True, max_length= 20, verbose_name="رقم الصك ")
    dDate = models.DateField(verbose_name="تاريخ الصك",blank=True,null=True)
    bName = models.CharField(max_length=50, verbose_name=" اسم المبنى ")
    bAddress = models.CharField(max_length=50,  blank=True,verbose_name="عنوان المبنى" )
    bNote = models.TextField(max_length=500, blank=True,verbose_name="ملاحظة ")
    dImage = models.FileField(upload_to= 'Idphotos/%y/%m/%d',  blank=True,verbose_name="صورة الصك ")
    bimage = models.FileField(upload_to= 'Idphotos/%y/%m/%d',  blank=True,verbose_name="صورة المبنى ")

    def __str__(self):
        return self.bName
    class Meta:
        verbose_name = 'المباني'



class Units (models.Model):
    kind = [
        ("تجاري","تجاري"),
        ("سكني","سكني"),
        ("سكني وتجاري","سكني وتجاري"),
    ]
    kind2 = [
        ("شقة","شقة"),
        ("محل","محل"),
        ("دور ","دور "),
        ("عمارة ","عمارة "),
        ("فندق ","فندق "),
        ("أخرى ","أخرى "),
    ]
    building = models.ForeignKey(Buildings,on_delete= models.SET_DEFAULT, default= True, verbose_name="المبنى  ")
    uKind = models.CharField(max_length=50,  choices=kind, verbose_name="سكني ام تجاري")
    uKind2 = models.CharField(max_length=50, choices=kind2, verbose_name="نوع الوحدة  ")
    uName = models.CharField(primary_key=True, max_length=50,verbose_name=" اسم الوحدة ")
    uNumber = models.IntegerField( max_length=10, verbose_name="رقم الوحدة - يجب ان يكون رقم خاص للوحدة ")
    uRoomsNo = models.IntegerField(max_length=10, blank= True, verbose_name=" عدد الغرف ")
    uFloor = models.IntegerField(max_length=10, blank= True,verbose_name="الدور  ")
    uElectricity = models.BigIntegerField(max_length=10, blank= True, verbose_name="رقم سداد الكهرباء  ",null=True,)
    uWater = models.BigIntegerField(max_length=10, blank= True, verbose_name=" رقم سداد المياه ",null=True,)
    
    def __str__(self):
        return self.uName
    class Meta:
        verbose_name = 'الوحدات'







class Contracts(models.Model):
    kind = [
        ("تجاري","تجاري"),
        ("سكني","سكني"),
    ]
    statuspaymint = [
    ("تم السداد","تم السداد"),
    ("لم يتم السداد","لم يتم السداد"),
    ("الغي","الغي"),
    ]
    contract_kind = models.CharField(max_length=50,  choices=kind, verbose_name="سكني ام تجاري")
    contractNumber = models.BigIntegerField(max_length=50, verbose_name= "رقم العقد الالكتروني")
    customer = models.ForeignKey(Customers, on_delete= models.PROTECT, default= True, verbose_name="المستأجر")
    unit = models.ForeignKey(Units, on_delete= models.SET_DEFAULT, default= True, verbose_name="الوحدة")
    startDate = models.DateField(verbose_name="تاريخ البدء")
    endDate = models.DateField(verbose_name="تاريخ الانتهاء")
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name="القيمة الإيجارية لكامل العقد")
    cFile = models.FileField(upload_to= 'contract/%y/%m/%d',  blank=True,verbose_name="العقد  ")
    cNote = models.TextField(max_length=500, blank=True,verbose_name="ملاحظة ")
    
    @property
    def vat(self):
        if self.contract_kind == "تجاري":
            return self.payment_amount * Decimal('0.15')
        else:
            return 0

    @property
    def total_amount(self):
        return self.payment_amount + self.vat
    
    @property
    def duration_days(self):
        return (self.endDate - self.startDate).days
    
    def get_received_payments(self):
        return Payment_recived.objects.filter(payment__contract=self)
    
    
    
    def __str__(self):
        return f"{self.customer} - {self.unit}"
    

import uuid
class Payment(models.Model):
    payment_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_due = models.DateField(null=True, blank=True)
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE, default=True)
    
    
    def __str__(self):
        return f"{self.contract.customer} - {self.amount} - {self.payment_due}"


class Payment_recived(models.Model):
    method = [
        ("حواله","حواله"),
        ("كاش","كاش"),
        ("شيك","شيك"),
        ("أخرى","أخرى"),
    ]
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=True,related_name='payment_received')
    received_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50,  choices=method, verbose_name="طريقة السداد  ",null=True, blank=True)
    doc_number = models.CharField(max_length=50, unique=True,verbose_name="بيانات المستند  " )
    
    @staticmethod
    def get_received_payments_for_contract(contract_id):
        contract = Contracts.objects.get(id=contract_id)
        return contract.get_received_payments()
    

    def __str__(self):
        return f"{self.payment.amount} - {self.received_amount} - {self.received_date} - {self.payment_method}"


    

    
class Login(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)


class Expenses (models.Model):
    beneficiary = models.CharField(max_length=80 , verbose_name="اسم المستلم")
    bNumber = models.BigIntegerField(max_length= 10, verbose_name="رقم الجوال ")
    eamount = models.IntegerField(max_length= 10, verbose_name="المبلغ ")
    eamounttext = models.CharField(max_length= 100, verbose_name="المبلغ كتابة ", blank=True)
    info  = models.TextField(max_length=500, blank=True,verbose_name="مقابل ")
    eBuilding = models.ForeignKey(Buildings,on_delete= models.CASCADE,  verbose_name="المبنى  ")
    eDb = models.DateField(verbose_name="تاريخ الصرف")
    
    def __str__(self):
        return self.beneficiary
    class Meta:
        verbose_name = 'المصروفات'