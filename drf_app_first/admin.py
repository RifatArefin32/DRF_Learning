from django.contrib import admin
from .models import Order, OrderItem

# Inline admin class for OrderItem
"""
- Purpose: To allow `OrderItem` instances to be edited directly within the `Order` admin interface.
- admin.TabularInline: Displays `OrderItem` objects in a tabular format (rows and columns).
- model = OrderItem: Specifies that this inline is for the OrderItem model.
"""
class OrderItemInLine(admin.TabularInline):
    model = OrderItem

# Model admin class for Order
"""
- Purpose: Customizes the admin interface for the `Order` model.
- admin.ModelAdmin: Allows overriding and customizing how the model is managed in the admin interface.
- inlines = [OrderItemInLine]: Adds the OrderItem inline admin class to the Order admin interface. 
This means when editing an `Order` in the admin, we can also add, edit, or delete related OrderItem records directly on the same page.
"""
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]  # Add the inline class to the Order admin

# Register the Order model with the OrderAdmin class
"""
Registers the `Order` model with the admin site, specifying `OrderAdmin` as its associated admin class. 
This makes `Order` and its associated `OrderItem` objects manageable in the admin interface.
"""
admin.site.register(Order, OrderAdmin)
