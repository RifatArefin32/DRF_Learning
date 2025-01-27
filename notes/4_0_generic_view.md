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