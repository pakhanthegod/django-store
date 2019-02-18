from django.contrib import admin

from .models import Order, OrderList


class OrderListInline(admin.TabularInline):
    model = OrderList
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderListInline,)


admin.site.register(Order, OrderAdmin)