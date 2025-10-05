from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
# Create your models here.
class SellerProfileModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return f"{self.user.username}"

class BuyerProfileModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)

    def __str__(self):
        return f"{self.user.username}"

class CategoryModel(models.Model):
    category=models.CharField(max_length=30)
    image=models.ImageField(upload_to="category_image",null=True,blank=True)

    def __str__(self):
        return f"{self.category}"


class ProductModel(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    categoryName=models.ForeignKey(CategoryModel,on_delete=models.CASCADE,null=True)
    price=models.FloatField()
    offer=models.IntegerField(default=0)
    description=models.TextField()
    color=models.TextField()
    image=models.ImageField(upload_to="images",null=True,blank=True)
    others=models.JSONField(null=True,blank=True)
    rating=models.FloatField(default=0)
    review=models.JSONField(null=True,blank=True)

    def __str__(self):
        return f"{self.title}"
    
    @property
    def ownername(self):
        return self.owner.username
    
    @property
    def productId(self):
        return self.pk
    
    @property
    def category(self):
        return self.categoryName.category

    def validate_price(self,value):
        if value<0:
            raise ValidationError("Price cannot be negative")
        else:
            return value
        
    def validate_offer(self,value):
        if value<0 or value>100:
            raise ValidationError("enter a valid offer")
        else:
            return value
        
    @property
    def offerPrice(self):
        value=(self.price*self.offer)/100
        ans=self.price-value
        return ans

class CartModel(models.Model):
    product=models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    createdon=models.DateField(auto_now=True)
    quantity=models.IntegerField(default=0)

    def __str__(self):
        return  f"{self.product.title}-{self.user.username}"
    
    @property
    def productId(self):
        return self.product.pk
    
    @property
    def productTitle(self):
        return self.product.title
    
    @property 
    def price(self):
        return self.product.price
    
    @property
    def image(self):
        return self.product.image
    
    @property
    def offerPrice(self):
        value=(self.product.price*self.product.offer)/100
        ans=self.product.price-value
        return ans