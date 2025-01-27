# Generic Views
Generic Views provide a powerful way to handle common patterns for building APIs, such as `retrieving`, `creating`, `updating`, and `deleting` objects. They are built on top of DRF's mixins and abstract a lot of repetitive boilerplate code, enabling us to focus on our application's core logic.

# Why Use Generic Views?
Generic Views reduce the need to write repetitive code for handling CRUD operations. They provide the following functionality:
- Retrieve a list of objects or a single object.
- Create a new object.
- Update an existing object.
- Delete an object.

# Commonly Used Generic Views
- ListAPIView
- RetrieveAPIView
- CreateAPIView
- UpdateAPIView
- DestroyAPIView
- ListCreateAPIView
- RetrieveUpdateAPIView
- RetrieveDestroyAPIView
- RetrieveUpdateDestroyAPIView

# Example Scenario
Let's assume we have a `Book` model, and we want to expose an API to perform CRUD operations on it.

## Define the Model
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title

```

## Create a Serializer
```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

```

## Use Generic Views
```python
from rest_framework.generics import ListCreateAPIView
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

```
- `GET` request to `/books/`: Returns a list of all books.
- `POST` request to `/books/`: Creates a new book.

### Retrieve, Update, and Delete API (RetrieveUpdateDestroyAPIView)
```python
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

```
- `GET` request to `/books/<id>/`: Retrieves a book by its ID.
- `PUT` or `PATCH` request to `/books/<id>/`: Updates the book.
- `DELETE` request to `/books/<id>/`: Deletes the book.

# Configure URLs
```python
from django.urls import path
from .views import BookListCreateView, BookDetailView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]

```

# Example Scenario with some attributes
- lookup_field
- lookup_url_kwarg
- pagination_class 
- filter_backends

## lookup_field and lookup_url_kwarg
Use these attributes for custom lookups when working with detail views.
```python
from rest_framework.generics import RetrieveAPIView

class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'isbn'  # Use 'isbn' field for lookup
    lookup_url_kwarg = 'book_isbn'  # URL keyword for lookup

# URL Configuration
from django.urls import path
from .views import BookDetailView

urlpatterns = [
    path('books/<book_isbn>/', BookDetailView.as_view(), name='book-detail'),
]

```
- This view will look up `books` by their isbn field when the URL contains `<book_isbn>`. 
- For example, Request to `/books/1234567890123/` will retrieve the book with `isbn="1234567890123"`.


# pagination_class
Add pagination to list views.

### Pagination Class
First, create a custom pagination class (optional).
```python
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'  # Allow the client to control page size
    max_page_size = 10  # Maximum page size limit

```
### View with Pagination
Apply the pagination to your view.
```python
from rest_framework.generics import ListAPIView

class PaginatedBookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination

```
- A `GET` request to `/books/` will return paginated results with `5` books per page. Clients can control page size by passing `?page_size=3`.
