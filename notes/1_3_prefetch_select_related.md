# prefetch_related() and select_related() in DRF
In Django (and by extension, Django REST framework), `prefetch_related()` and `select_related()` are used to optimize database queries involving relationships between models. They help reduce the number of queries sent to the database when fetching related data.

<br>
<br>
<br>

# When to Use
- Use `select_related()` when accessing a `single related object` via a `ForeignKey` or `OneToOneField`.
- Use `prefetch_related()` when accessing `multiple related objects` via a `ManyToManyField` or `reverse ForeignKey`.

<br>
<br>
<br>

# select_related()
- Used for single-valued relationships, such as `ForeignKey` and `OneToOneField`.
- Performs a SQL JOIN to fetch related data in a single query.
- Improves performance by avoiding additional queries for related fields.

### Example
**Models**
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

**View without select_related()**
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()  # Fetches books
        data = [{"title": book.title, "author": book.author.name} for book in books]
        return Response(data)
```
For every `book`, a query is executed to fetch the related `author`. If there are `10` books, this results in `1` query for books + `10` queries for authors = `11` queries. This is called `Lazy Loading`.

**View with select_related()**
```python
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.select_related('author')  # Single query with JOIN
        data = [{"title": book.title, "author": book.author.name} for book in books]
        return Response(data)
```
Now, only `1` query is executed to fetch books and their authors. 

<br>
<br>
<br>

# prefetch_related()
- Used for multi-valued relationships, such as `ManyToManyField` and `reverse ForeignKey(related_name)`.
- Executes a separate query for the related objects and performs in-Python joining.

### Example
**Models**
```python
class Publisher(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    publishers = models.ManyToManyField(Publisher, related_name='books')
```

**View without prefetch_related()**
```python
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()  # Fetches books
        data = [{"title": book.title, "publishers": [pub.name for pub in book.publishers.all()]} for book in books]
        return Response(data)
```
For every `book`, a query is executed to fetch the related `publishers`. If there are `10` books with `3` publishers each, this results in `1` query for books + `10` queries for publishers = `11` queries.

**View with prefetch_related()**
```python
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.prefetch_related('publishers')  # Single query for books + 1 query for publishers
        data = [{"title": book.title, "publishers": [pub.name for pub in book.publishers.all()]} for book in books]
        return Response(data)
```
Now, only `2` queries are executed: one for `books` and one for `publishers`.

<br>
<br>
<br>

# Combining `select_related()` and `prefetch_related()`
We can use both together when we need to optimize queries for both `single-valued` and `multi-valued` relationships.

### Example
```python
books = Book.objects.select_related('author').prefetch_related('publishers')
```
This fetches the author with a SQL JOIN and the publishers with a separate query.