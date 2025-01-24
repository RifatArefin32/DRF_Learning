# Django Model Relationship
In Django, models can be related to one another in several ways, depending on the nature of the relationship between the entities. Django provides **three** primary types of relationships.
- One-to-One 
- Many-to-One, and 
- Many-to-Many. 


<br>


# One-to-One Relationship
In a one-to-one relationship, each instance of a model is related to exactly one instance of another model. This type of relationship is less common but useful when we want to ensure that one record is associated with a unique record in another model.

### Example
Suppose each `User` of a website has his unique `User Profile` i.e. Each `UserProfile` belongs to a `User`. So we would model this as a **one-to-one relationship**.

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    bio = models.TextField()

    def __str__(self):
        return f"Profile of {self.user.username}"

```
Here, in our `UserProfile` model, we've created a `OneToOneField` that links the `UserProfile` model to the `User` model using the `user` field. 

## Accessing the `User` from a `UserProfile`

```python
user_profile = UserProfile.objects.get(id=1) 
user = user_profile.user
```

## Accessing the `UserProfile` from a `User`
The reverse relationship from the `User` model to the `UserProfile` model will automatically be created by Django, using the lowercase name of the related model i.e. `userprofile` in this case by default.

```python
user_instance = User.objects.get(username="some_username")
user_profile = user_instance.userprofile
```

## Reverse relationship with `related_name` property 
With related_name, we can specify the `related_name` parameter in the OneToOneField, by which we can make reverse relationship.

```python
# In the UserProfile model,
user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

# access `UserProfile` from a `User` instance
user_profile = user_instance.profile
```


<br>


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
## Accessing a `Customer` from an `Order`
Given an `Order` instance, we can access the associated `Customer` using the `customer` attribute.

```python
order = Order.objects.get(id=1)
customer = order.customer
```

## Accessing `Orders` from a `Customer`
We can access the orders of a specific customer using the `order_set` attribute (default reverse relationship) or a custom related_name (if specified).

```python
# Retrieve a Customer instance
customer = Customer.objects.get(username="john_doe")

# Access all orders for this customer
orders = customer.order_set.all()  # Default reverse relationship
```

## Reverse relationship with `related_name` property 
With related_name, we can specify the `related_name` parameter in the `ForeignKey`, by which we can make reverse relationship.

```python
# In the UserProfile model,
customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")

# Access all orders using the custom related_name
customer = Customer.objects.get(username="john_doe")
orders = customer.orders.all()  # 'orders' is the related_name
```


<br>


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
- There is no strict convention that a `ManyToManyField` must only be defined in a specific class. We define the it in either of the related classes, depending on the context and the design of our application. 





## How `ManyToManyField` works?
When we use a `ManyToManyField`, Django automatically creates an intermediary table to manage the `many-to-many` relationship. This table is used behind the scenes to link the two models involved in the `many-to-many` relationship. When we define a `ManyToManyField`, Django automatically creates a `join table` to store the relationship between the two models. This join table typically has two foreign keys—one pointing to each of the models involved in the `many-to-many` relationship. Django will create an automatic table, usually named `<appname>_<modelname>_<modelname>`.

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
orders_for_product = product.order_set.all()  # Access all related orders if the `related_name` property missing
```


<br>


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