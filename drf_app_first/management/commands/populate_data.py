# myapp/management/commands/populate_dummy_data.py
from django.core.management.base import BaseCommand
from drf_app_first.models import User, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create Users
        user = User.objects.create_user(username="john_doe", password="password", email="john@example.com")
        
        # Create Products
        product1 = Product.objects.create(name="Product 1", description="Description for Product 1", price=100.0, stock=10)
        product2 = Product.objects.create(name="Product 2", description="Description for Product 2", price=50.0, stock=20)
        product3 = Product.objects.create(name="Product 3", description="Description for Product 3", price=30.0, stock=5)
        
        # Create an Order
        order = Order.objects.create(user=user, status=Order.StatusChoices.PENDING)
        
        # Create OrderItems
        OrderItem.objects.create(order=order, product=product1, quantity=2)
        OrderItem.objects.create(order=order, product=product2, quantity=1)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))
