# Serializers
- Serializers allow complex data such as `querysets` and `model` instances to be converted to `native Python datatypes` which can be easily rendered into `JSON`, `XML` or other content types. 
- Serializers also provide deserialization, allowing `parsed data` i.e. `JSON`, `XML` to be converted back into complex types, after validating the incoming data.
- The serializers in DRF work very similarly to `Django's Form` and `ModelForm` classes. 
- Serializer class gives us a generic way to control the output of our responses.
- `ModelSerializer` class provides a useful shortcut for creating serializers that deal with model instances and querysets.