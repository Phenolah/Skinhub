from django.contrib import admin
from .models import *

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
make_refund_accepted.short_description ='Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'discount_coupon',
                    'payment',
                    'ref_code']
    list_display_links = [
        'customer',
        'payment',
        'discount_coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'customer',
        'ref_code'
    ]
    actions = [make_refund_accepted]


# Register your models here.
admin.site.register(Item)
admin.site.register(OrderItem)
#admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(DiscountCode)
admin.site.register(Order,OrderAdmin)
