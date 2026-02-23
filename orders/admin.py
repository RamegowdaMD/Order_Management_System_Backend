from django.contrib import admin
from .models import Order,OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','status','address','created_at','total_price')
    search_fields = ('user__username','status')
    readonly_fields = ('total_price', 'created_at')
    inlines = [OrderItemInline]



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','quantity','price','product')




