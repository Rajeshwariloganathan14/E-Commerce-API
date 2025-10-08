from .models import ProductModel,CartModel,CategoryModel,OrdersModels
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    ownername=serializers.ReadOnlyField()
    productId=serializers.ReadOnlyField()
    offerPrice=serializers.ReadOnlyField()
    category=serializers.ReadOnlyField()
    class Meta:
        model=ProductModel
        fields=["ownername","productId","title","brand","category","price","offer","description","color","image","others","offerPrice","rating","review"]
        
class CartSerializer(serializers.ModelSerializer):
    productTitle=serializers.ReadOnlyField()
    productId=serializers.ReadOnlyField()
    price=serializers.ReadOnlyField()
    image=serializers.ImageField(read_only=True)
    offerPrice=serializers.ReadOnlyField()
    class Meta:
        model=CartModel
        fields=["productId","productTitle","price","quantity","offerPrice","image"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoryModel
        fields=["category","image","id"]

class DetailedProductSerializer(serializers.ModelSerializer):
    price=serializers.ReadOnlyField()
    image=serializers.ImageField(read_only=True)
    offerPrice=serializers.ReadOnlyField()
    class Meta:
        model=ProductModel
        fields=["id","title","price","offerPrice","image"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrdersModels
        fields=["product","finalPrice","quantity","orderPlacedDate","days"]