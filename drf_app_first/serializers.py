from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'in_stock']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price')
    class Meta:
        model = OrderItem
        fields = ['product_name', 'product_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    product = ProductSerializer(many=True, read_only=True)
    # product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    """
    NOTE: We use SerializerMethodField to get the value defined in the model
    Conventionally the method name is 'get_total_price', if we want to give 
    another name, then mention it in the serializer as follows:
    total_price = serializers.SerializerMethodField(method_name='custom_method')
    
    def custom_method(self, obj):
        # do something
    """
    class Meta:
        model = Order
        fields = ['order_id', 'user', 'status', 'product', 'items', 'total_price']



class PorductInfoSerializer(serializers.Serializer):
    # get all products, count of products, max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
     