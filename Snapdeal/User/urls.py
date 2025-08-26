from django.urls import path
from . import views

urlpatterns=[
    path("email/",views.EmailView.as_view(),name="Email"),
    path("otp/",views.OTPView.as_view(),name="otp"),
    path("setPassword/",views.SetPasswordView.as_view(),name="Sign Up")
    
]






