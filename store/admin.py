from django.contrib import admin
from .models import Products,Categary,Custmer,Order


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'categary']


class AdminCategary(admin.ModelAdmin):
    list_display = ['name']


class AdminCustmer(admin.ModelAdmin):
    list_display = ['email']

admin.site.register(Products,AdminProduct)
admin.site.register(Categary,AdminCategary)
admin.site.register(Custmer,AdminCustmer)
admin.site.register(Order)