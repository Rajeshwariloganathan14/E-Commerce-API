from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.SellerProfileModel)
admin.site.register(models.BuyerProfileModel)
admin.site.register(models.ProductModel)
admin.site.register(models.CartModel)
admin.site.register(models.CategoryModel)
admin.site.register(models.OrdersModels)
