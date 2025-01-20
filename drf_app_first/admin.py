from django.contrib import admin
from .models import Order, OrderItem

# Inline admin class for OrderItem
class OrderItemInLine(admin.TabularInline):
    model = OrderItem

# Model admin class for Order
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]  # Add the inline class to the Order admin

# Register the Order model with the OrderAdmin class
admin.site.register(Order, OrderAdmin)
