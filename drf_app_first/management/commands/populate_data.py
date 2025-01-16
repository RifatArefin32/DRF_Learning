# myapp/management/commands/populate_dummy_data.py
from faker import Faker
from django.core.management.base import BaseCommand
from drf_app_first.models import User, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create Users
        user = User.objects.create_user(username="john_doe", password="password", email="john@example.com")
        """
        create_user() method is specifically designed to handle user creation, ensuring that passwords are hashed 
        before being saved to the database. When we use create_user(), the password is automatically hashed using 
        Django's password hashing mechanisms (via set_password()).
        """
        
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

        # Create data using faker
        fake = Faker()

        # Generate fake users
        user = User.objects.create_user(username=fake.user_name(), password=fake.password(), email=fake.email())
        self.stdout.write(self.style.SUCCESS(f"User {user.username} created"))

        # Create 5 fake products
        for _ in range(5): 
            product = Product.objects.create(
                name=fake.word(),
                description=fake.text(max_nb_chars=200),
                price=fake.random_number(digits=3),
                stock=fake.random_int(min=0, max=100)
            )
            self.stdout.write(self.style.SUCCESS(f"Product {product.name} created"))

        # Create 3 fake orders and order items
        for _ in range(3): 
            order = Order.objects.create(user=user, status=Order.StatusChoices.PENDING)
            self.stdout.write(self.style.SUCCESS(f"Order {order.order_id} created"))

            # Create fake order items
            for product in Product.objects.all():
                quantity = fake.random_int(min=1, max=5)
                order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
                self.stdout.write(self.style.SUCCESS(f"OrderItem for {product.name} created"))

        self.stdout.write(self.style.SUCCESS('Fake data has been generated successfully!'))

