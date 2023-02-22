from django.contrib import admin
from .models import *

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']

    
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
