from django.contrib import admin
from . models import *

admin.site.register(Charity)

# Register your models here.
@admin.register(RequestFund)
class RequestFund(admin.ModelAdmin):
     list_display = ('name', 'email', 'phone', 'state', 'city', 'address', 'chariti', 'date')


@admin.register(Donor)
class Donor(admin.ModelAdmin):
     list_display = ('donor', 'date_of_birth', 'phone', 'city', 'state', 'address', 'chariti', 'gender', 'image', 'ready_to_donate')

@admin.register(Donation_list)
class Charity(admin.ModelAdmin):
     list_display = ('name', 'date', 'amount', 'email', 'chariti', 'state', 'city')