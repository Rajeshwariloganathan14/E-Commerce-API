from django.db import models
from django.contrib.auth.models import User
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