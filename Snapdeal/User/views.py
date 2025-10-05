from django.shortcuts import render
from rest_framework.views import APIView
import random
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage  
from django.conf import settings
from .models import BuyerProfileModel,SellerProfileModel,ProductModel,CartModel,CategoryModel
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer,CartSerializer,CategorySerializer

# Create your views here.

def generateOTP():
    otp=""
    for i in range(6):
        otp+=str(random.randint(0,9))
    return otp

def join(arr):
    if type(arr)==type("str"): 
        arr=arr.split(",")
    str=""
    for i in arr:
        str+=i
    return str

class EmailView(APIView):
    def post(self,request):
        data=request.data
        if not data.get("email"):
            return Response({"email":"Failed","error":"email required"},status.HTTP_400_BAD_REQUEST)
        user=User.objects.filter(email=data.get("email")).first()
        if user:
            return Response({"email":"Failed","error":"email already exists"},status.HTTP_400_BAD_REQUEST)
        otp=generateOTP()
        print(otp)
        cache.set(data.get("email"),otp,600)
        subject="otp for signup"
        body=f"<h1>OTP:{otp}</h1>"
        email=EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=[data.get("email")],
        )        
        email.content_subtype="html"
        email.send()
        return Response({"email":"OTP send successfully","otp":otp},status.HTTP_200_OK)
    
class OTPView(APIView):
    def post(self,request):
        data=request.data
        email=data.get("email")
        if email is None:
            return Response({"otp":"Failed","error":"email required"},status.HTTP_400_BAD_REQUEST)
        if not join(data.get("otp")):
            return Response({"otp":"Failed","error":"otp is  required"},status.HTTP_400_BAD_REQUEST)
        if join(data.get("otp")) != cache.get(email):
            print(cache.get(email))
            return Response({"otp":"Failed","error":"Wrong OTP"},status.HTTP_400_BAD_REQUEST)
        return Response({"otp":"Successful"},status.HTTP_200_OK)        

class SetPasswordView(APIView):
    def post(self,request):
        data=request.data
        email=data.get("email")
        if email is None:
            return Response({"password":"Failed","error":"email required"},status.HTTP_400_BAD_REQUEST)
        data=request.data
        if not data.get("password") or not data.get("confirmPassword"):
            return Response({"password":"Failed","error":"password and confirmPassword required"},status.HTTP_400_BAD_REQUEST)
        if data.get("password")!=data.get("confirmPassword"):
            return Response({"password":"Failed","error":"password and confirmPassword should be same"},status.HTTP_400_BAD_REQUEST)
        if not join(data.get("otp")):
            return Response({"password":"Failed","error":"otp is  required"},status.HTTP_400_BAD_REQUEST)
        if join(data.get("otp")) != cache.get(email):
            print(cache.get(email))
            return Response({"password":"Failed","error":"Wrong OTP"},status.HTTP_400_BAD_REQUEST)
        user=User(username=email)
        user.set_password(data.get("password"))
        user.save()
        if(data.get("customerType")=="buyer"):
            BuyerProfileModel(
                user=user
            ).save()
        elif(data.get("customerType")=="seller"):
            SellerProfileModel(
                user=user
            ).save()
        return Response({"password":"Successful"},status.HTTP_201_CREATED)

class CreateProductView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=self.request.user
        data=request.data
        seller=SellerProfileModel.objects.filter(user=user).first()
        if not seller:
            return Response({"error":"only sellers can add products"},status.HTTP_400_BAD_REQUEST)
        ProductModel(
            owner=user,
            title=data.get("title"),
            brand=data.get("brand"),
            category=data.get("category"),
            price=data.get("price"),
            offer=data.get("offer"),
            description=data.get("description"),
            color=data.get("color"),
            image=data.get("image"),
            others=data.get("others")
        ).save()

        return Response({"addPost":"Successful"},status=status.HTTP_201_CREATED)
        
class ViewProduct(APIView):
    def get(self, request,id=None):
        data=request.data
        if id:
            products=ProductModel.objects.filter(pk=id)
            if not products:
                return Response({"Products":"Not found"},status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(products)
            return Response(serializer.data,status.HTTP_404_NOT_FOUND)
        else:
            products=ProductModel.objects.all()
            if not products:
                return Response({"Products":"Not found"},status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(products,many=True)
            return Response(serializer.data,status.HTTP_200_OK) 
        
class DeleteProductView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,id=None):
        user=request.user                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        data=request.data
        product=ProductModel.objects.filter(pk=id).first()
        if product.owner!=user:
            return Response({"error":"only owner can delete the product"},status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response({"ProductDelete":"Successful"},status.HTTP_200_OK) 
    
class AddCartView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,id=None):
        user=request.user
        data=request.data
        product=ProductModel.objects.filter(pk=id).first()
        if not product:
            return Response({"error":"No product found"},status.HTTP_404_NOT_FOUND)
        CartModel(
            product=product,
            user=user,
            quantity=data.get("quantity")
        ).save()
        return Response({"AddToCart":"Successful"},status.HTTP_200_OK)
    
class ListCartProductsView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data=request.data
        user=request.user
        cart=CartModel.objects.filter(user=user).all()
        if not cart:
            return Response({"error":"Nothing in cart"})
        print(cart)
        serializer=CartSerializer(cart,many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    
class EditCartProductView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,id=None):
        data=request.data
        user=request.user
        product=ProductModel.objects.filter(pk=id).first()
        if not product:
            return Response({"error":"Product not found"},status.HTTP_404_NOT_FOUND)
        cart=CartModel.objects.filter(product=product,user=user).first()
        if not cart:
            return Response({"error":"Product not found in the cart"},status.HTTP_404_NOT_FOUND)
        cart.quantity=data.get("quantity")
        cart.save()
        return Response({"editCartProduct":"Successful"},status.HTTP_200_OK)
        
class DeleteCartProductView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,id=None):
        data=request.data
        user=request.user
        product=ProductModel.objects.filter(pk=id).first()
        if not product:
            return Response({"error":"Product not found"},status.HTTP_404_NOT_FOUND)
        cart=CartModel.objects.filter(product=product,user=user).first()
        if not cart:
            return Response({"error":"Product not found in the cart"},status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response({"deleteCartProduct":"Successful"},status.HTTP_200_OK)
    
class CategoriesListView(APIView):
    def get(self,request):
        category=CategoryModel.objects.all()
        if not category:
            return Response({"error":"No categories"},status.HTTP_204_NO_CONTENT)
        serializer=CategorySerializer(category,many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    
class CategoryProductListView(APIView):
    def get(self,request,id=None):
        category=CategoryModel.objects.filter(pk=id).first()
        if not category:
            return Response({"error":"No categories"},status.HTTP_204_NO_CONTENT)
        products=ProductModel.objects.filter(categoryName=category).all()
        if not products:
            return Response({"error":"No product in the category"},status.HTTP_204_NO_CONTENT)
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    
