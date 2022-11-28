from django.contrib import admin

from .models import *
admin.site.register(Item)
admin.site.register(Currency)
admin.site.register(Order)
admin.site.register(OrderItemsList)
admin.site.register(Discount)
admin.site.register(Tax)

