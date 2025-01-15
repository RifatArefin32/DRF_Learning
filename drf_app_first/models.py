from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# create custom User model
class User(AbstractUser):
    pass


# create Product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    """
    The @property decorator in Python allows us to define a method that behaves like an attribute. 
    This means that we can access the result of the method without calling it as a function (i.e., without using parentheses).
    For example:
        product = Product.objects.get(id=1)
        if product.in_stock:
            print("In stock")
        else:
            print("Out of stock")
    """
    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    