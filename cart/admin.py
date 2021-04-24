from django.contrib import admin
from .models import items,OrderItem,Order,Address,payment,Category,Comment

admin.site.register(Category)
admin.site.register(items)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(payment)
admin.site.register(Address)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment','status', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('comment','ip','status','user','product','rate','id')

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'create_at']
    # list_filter = ['status']
    readonly_fields = ('comment','ip','user','item','rate','id')

admin.site.register(Comment,CommentAdmin)


# Register your models here.
