from django.shortcuts import render
from rest_framework.views import APIView
import random
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings
from .models import BuyerProfileModel,SellerProfileModel

# Create your views here.

def generateOTP():
    otp=""
    for i in range(6):
        otp+=str(random.randint(0,9))
    return otp

def join(arr):
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



