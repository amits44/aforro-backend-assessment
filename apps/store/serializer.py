from rest_framework import serializers
from.models import Inventory,Store

class StoreInventorySerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="prduct.title", read_only = True)
    price = serializers.CharField(source='product.price', read_only=True)
    category_name = serializers.CharField(source='product.category.name', read_only =True)

    class Meta:
        model = Inventory
        fields= ['product_title','price','category_name','quantity']