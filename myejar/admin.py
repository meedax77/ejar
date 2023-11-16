from django.contrib import admin
from .models import Customers, Expenses ,Payment_recived, Buildings, Units, Contracts, Payment, Login
# Register your models here.



admin.site.register(Customers)
admin.site.register(Buildings)
admin.site.register(Units)
admin.site.register(Contracts)
admin.site.register(Payment)
admin.site.register(Login)
admin.site.register(Payment_recived)
admin.site.register(Expenses)