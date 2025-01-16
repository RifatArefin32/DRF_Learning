# Django Model Relationship
In Django, models can be related to one another in several ways, depending on the nature of the relationship between the entities. Django provides **three** primary types of relationships.
- One-to-One 
- Many-to-One, and 
- Many-to-Many. 

# One-to-One Relationship
In a one-to-one relationship, each instance of a model is related to exactly one instance of another model. This type of relationship is less common but useful when we want to ensure that one record is associated with a unique record in another model.

### Example
Suppose each `User` of a website has his unique `User Profile`. So we would model this as a **one-to-one relationship**.

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    bio = models.TextField()

    def __str__(self):
        return f"Profile of {self.user.username}"

```

# Many-to-One Relationship
In a many-to-one relationship, multiple instances of one model can be related to a single instance of another model. This is one of the most common relationships and is represented using the `ForeignKey` field in Django.

### Example
A `Customer` can place many `Orders`, but each `Order` is linked to exactly one `Customer`.

```python
# Customer class
class Customer(models.Model):
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Order class
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"

```

# Many-to-Many Relationship
A many-to-many relationship allows multiple instances of one model to be related to multiple instances of another model. This is represented using the `ManyToManyField `in Django, and Django automatically creates a join table to handle this relationship.

### Example
A `Student` can enroll in many `Courses`, and each `Course` can have many `Students`.

```python
# Course model
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name



# Student model
class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.name

```
- The `ManyToManyField` creates a many-to-many relationship between `Student` and `Course`. 
- Each `Student` can enroll in multiple `Course` instances, and each `Course` can have many `Student` instances.
- Django automatically creates an intermediary table to store the relationships.


# `related_name` Attribute
The `related_name` attribute in Django is used to define the name of the reverse relation from the related model back to the model that contains the `OneToOneField`, `ForeignKey` or `ManyToManyField` field. It allows us to specify how to access the related objects from the other side of the relationship.


## Without related_name
Django uses the default reverse relation name, which is `<model_name>_set` in lowercase.

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


author = Author.objects.get(id=1)
books_by_author = author.book_set.all()  # all books related to this author
```
In this case, Django will automatically create a reverse relation named `book_set`. This means that if we have an `Author` instance, we can access all of the related `Book` instances using `author.book_set.all()`.




## With related_name
If we want to give the reverse relation a more meaningful name, we can specify the `related_name` attribute.

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')


author = Author.objects.get(id=1)
books_by_author = author.books.all()  # all books related to this author

```
Now, we can access all books related to an Author instance using `author.books.all()` instead of the default `book_set`.



# How ManyToManyField works?
When we use a ManyToManyField, Django automatically creates an intermediary table to manage the `many-to-many` relationship. This table is used behind the scenes to link the two models involved in the `many-to-many` relationship. When we define a `ManyToManyField`, Django automatically creates a `join table` to store the relationship between the two models. This join table typically has two foreign keys—one pointing to each of the models involved in the `many-to-many` relationship. Django will create an automatic table, usually named `<appname>_<modelname>_<modelname>`.

### Example

```python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    products = models.ManyToManyField(Product, related_name='orders')

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

```
Here, Django will automatically create a join table in the database to manage the many-to-many relationship between `Order` and `Product`. The join table will likely have two foreign key columns:
- One foreign key pointing to the `Order` model.
- One foreign key pointing to the `Product` model.
This join table will contain records that represent which products are part of which orders.

 

## How to Access the Many-to-Many Relationship
```python
# Access all products in a specific order
order = Order.objects.get(id=1)
products_in_order = order.products.all()  # Access all related products

# Access all orders for a specific product
product = Product.objects.get(id=1)
orders_for_product = product.orders.all()  # Access all related orders
```

# Use of `through` attribute
There are some scenarios where we need to store additional information about the relationship between two models. This is where the `through` attribute comes into play.

### Example
In the case of an order containing products, we might want to track the quantity of each product in the order, as well as the price of each product at the time the order was placed. This kind of additional data can't be stored in Django's automatic many-to-many relationship table, but you can handle it by using a custom `through model`.

```python
# Product model
class Product(models.Model):
    product_code = models.CharField(max_length=10)
    name = models.CharField(max_length=25, unique=True)


# Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')


# OrderItem table for the custom through model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

```
Here, `OrderItem` is the `custom through model` that allows us to store additional data (quantity) about the relationship between Order and Product. The `ManyToManyField` in Order uses `through='OrderItem'` to specify that the relationship between `Order` and `Product` should be managed through the `OrderItem` model, which contains the quantity of each product in the order. In this case, the automatic join table is replaced by the custom `OrderItem` table, which can store more detailed information.


# How to Populate Dummy Data for Django Models using Custom Management Command?
- Create a custom management command inside our app, create a `management/commands` directory.
- Create a new Python file for our command, e.g., `populate_dummy_data.py`.
```python
# myapp/management/commands/populate_dummy_data.py
from django.core.management.base import BaseCommand
from myapp.models import User, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create Users
        user = User.objects.create_user(username="john_doe", password="password123", email="john@example.com")
        
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

```
- After creating the custom command, run the command using:
```bash
python manage.py populate_dummy_data
```
