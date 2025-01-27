# Django REST Framework Request Object
The DRF request object is an instance of `rest_framework.request.Request`, which wraps Django's standard `HttpRequest` and provides API-specific features like `content negotiation`, `parsed data handling`, and `serializers`.

# Key Features of the DRF request Object
## request.method
Same as Django's HttpRequest object; returns the HTTP method (e.g., GET, POST, etc.).
<br>

## request.data
- Handles parsed request data from the body.
- Automatically parses `JSON`, `form data`, and other formats based on the `content-type` header.
- Preferred over `request.POST` in DRF.

### Example
```python
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    def post(self, request, format=None):
        # Access parsed data
        name = request.data.get('name')
        return Response({'message': f'Hello, {name}'})
```
<br>

## request.query_params
Works like `request.GET` in Django but is preferred in DRF for consistency. It is used to access query parameters from the URL of a request. When a client sends a request to a `DRF view` with query parameters (key-value pairs appended to the URL after a ?), `request.query_params` allows us to retrieve those parameters.

### Example
```bash
GET /api/items/?category=books&limit=10
```
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    def get(self, request):
        category = request.query_params.get('category')  # 'books'
        limit = request.query_params.get('limit')       # '10'
        
        # Use the parameters in your logic
        return Response({"category": category, "limit": limit})
```
<br>

## request.user
Represents the currently authenticated user. It returns:
- The user instance for authenticated users.
- An instance of `rest_framework.authentication.Token` or `rest_framework.authentication.SessionAuthentication`.
- AnonymousUser if the user is not authenticated.

### Example
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })
```
If the user is authenticated, `request.user` will be the `User` instance corresponding to their credentials. The respone will be,
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```
<br>

## request.auth
### Authenticated Requests
If the request is successfully authenticated, `request.auth` will contain authentication-specific information, such as:
- A token instance if TokenAuthentication is used.
- A session object if SessionAuthentication is used.
The exact value depends on the authentication class in use.

### Unauthenticated Requests
If the request is unauthenticated, `request.auth` will be `None`.

### Examples 
### Token Authentication
Suppose the request includes a valid token in the Authorization header.
```
Authorization: Token abc123xyz
```
In a view,
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ExampleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # The authenticated user instance
        auth = request.auth  # The token object
        
        return Response({
            "user": user.username,
            "auth": str(auth)  # Typically, this is the token string or object
        })
```
Example response,
```json
{
    "user": "john_doe",
    "auth": "abc123xyz"
}
```
### Session Authentication
When using `SessionAuthentication`, `request.auth` will typically be `None` because session authentication does not rely on a specific token or credential object.

### Custom Authentication Classes 
If we use a custom authentication class, `request.auth` will contain whatever value our custom class assigns during the authentication process. For example, this could be an object, a string, or even additional metadata.
<br>

## request.content_type
Returns the Content-Type header of the request.
### Example
```python
if request.content_type == 'application/json':
    # Process JSON data
```


# How data should be accessed in REST-based web services when using Django. 
Avoiding the use of `request.POST` in favor of other methods like request.body or request.data. 

## What is `request.POST`?
- `request.POST` is a **dictionary-like** object in Django that holds `form-encoded data` sent via an `HTTP POST` request.
- It is specifically designed to work with data sent using `application/x-www-form-urlencoded` or `multipart/form-data` (e.g., HTML forms or file uploads).

## Why is `request.POST` not ideal for REST APIs?
- REST APIs often deal with data in `JSON format` rather than form-encoded data. Here’s why `request.POST` is problematic.

- `request.POST` only parses form-encoded data. If the incoming request contains `JSON (content type: application/json)`, `request.POST` will be empty.
- If a REST client sends data in a non-form-encoded format (e.g., JSON or XML), using `request.POST` might lead to errors or cause data to be ignored.

## What should we use instead?
In REST APIs, we should use `request.body` or `request.data`.
### `request.body`
- It gives us raw access to the body of the HTTP request as a **byte string**. 
- It is useful if we want to manually parse the data (e.g., JSON).

```python
    import json
    body = json.loads(request.body)
```

### `request.data (Django REST Framework - DRF)`
- If we are using DRF, `request.data` is the preferred way to access parsed request data. 
- DRF automatically handles parsing JSON, form-encoded data, and other content types.

```python
data = request.data  # Works seamlessly for JSON and form-encoded data
```

If the request content type is `application/json` then the type of `request.data` is simply a python dictionary.
```json
// application/json
{
  "name": "John",
  "age": 30
}
```
```python
# request.data
{'name': 'John', 'age': 30}
```

### Example Comparison
Using request.POST (not ideal for REST APIs)
```python
def my_view(request):
    name = request.POST.get('name')  # Only works for form-encoded data
```    
Using request.body (better for JSON data)
```python
import json

def my_view(request):
    body = json.loads(request.body)
    name = body.get('name')
```
Using DRF's request.data (preferred for REST APIs with DRF)
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def my_view(request):
    name = request.data.get('name')  # Handles JSON, form-encoded, etc.
    return Response({'name': name})
```

<br>
<br>
<br>

# Request parsing
REST framework's `Request` objects provide flexible request parsing that allows us to treat requests with `JSON` data or other media types in the same way that we would normally deal with `form data`.

