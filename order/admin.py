from django.contrib import admin
from order.models import Flavor, Size, Topping, Pizza, Bread
from order.models import Customer, Order

admin.site.register(Flavor)
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Bread)
admin.site.register(Customer)
admin.site.register(Order)

