# `MEDIA_ROOT`, `MEDIA_URL`, and the `upload_to` Property in Django
These are essential configurations for handling user-uploaded files, particularly when using fields like `FileField` and `ImageField`.

## MEDIA_ROOT
`MEDIA_ROOT` is the absolute filesystem path to the directory where all user-uploaded files will be stored. It is the physical location on our server where files are saved.
- It must be an absolute path.
- Typically, this is a directory named `media/` located in our project's root directory.
- Files uploaded through models using `FileField` or `ImageField` are saved in subdirectories under this path, as determined by the `upload_to` property.

### Configure
```python
# settings.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
### File structure
```bash
# File structure
project_root/
├── manage.py
├── myapp/
├── media/
│   ├── images/
│   ├── user_1/
│   ├── ...
```

<br>
<br>
<br>

## MEDIA_URL
`MEDIA_URL` is the URL path used to serve media files. It provides the public-facing URL that corresponds to the `MEDIA_ROOT` directory.
- It is used to construct URLs for accessing media files via a browser.
- Often set to `/media/`, but we can customize it.
- It must end with a `/`.

### Configuration
```python
# settings.py
MEDIA_URL = '/media/'
```

### Example
If an image file is stored in `MEDIA_ROOT/images/example.jpg`, the URL to access it would be:
```
http://example_site.com/media/images/example.jpg
```

<br>
<br>
<br>

## `upload_to` Property
The `upload_to` property of fields like `FileField` and `ImageField` determines the **subdirectory** inside `MEDIA_ROOT` where uploaded files will be stored. 
- A static string for the directory.
- A callable function to dynamically generate the path.

### Example
```python
from django.db import models

class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/')
```
If a file named `user.jpg` is uploaded, it will be stored as,
```
MEDIA_ROOT/avatars/user.jpg
```

### Serving Media Files
During development, Django can serve media files using the `django.views.static.serve` view.

Configuration in `urls.py`

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your other URL patterns...
]

# Add this only in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

<br>
<br>
<br>

## Example
Suppose we have a `Product` model,
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    def __str__(self):
        return self.name

```

If Product is created with an image named product1.jpg, it will be stored at:
```bash
MEDIA_ROOT/products/product1.jpg
```

To access the image in templates,
```html
<img src="{{ product.image.url }}" alt="{{ product.name }}">
```