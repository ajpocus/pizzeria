from django.contrib import admin
from order.models import Customer, Order, Pizza, Bread, Topping

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Pizza)
admin.site.register(Bread)
admin.site.register(Topping)

