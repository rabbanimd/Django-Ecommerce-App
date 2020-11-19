from django.contrib import admin
from .models import items,OrderItem,Order,address,payment,Category

admin.site.register(Category)
admin.site.register(items)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(payment)
admin.site.register(address)



# Register your models here.
