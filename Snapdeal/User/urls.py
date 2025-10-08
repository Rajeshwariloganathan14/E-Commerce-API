from django.urls import path
from . import views

urlpatterns=[
    path("email/",views.EmailView.as_view(),name="Email"),
    path("otp/",views.OTPView.as_view(),name="otp"),
    path("setPassword/",views.SetPasswordView.as_view(),name="Sign Up"),
    path("product/create/",views.CreateProductView.as_view(),name="productCreate"),
    path("product/<str:id>/",views.ViewProduct.as_view(),name="viewProduct"),
    path("product/",views.ViewProduct.as_view(),name="viewProduct"),
    path("product/delete/<str:id>/",views.DeleteProductView.as_view(),name="product delete"),
    path("cart/add/<str:id>/",views.AddCartView.as_view(),name="cart add"),
    path("cart/list/",views.ListCartProductsView.as_view(),name="cart list"),
    path("cart/edit/<str:id>/",views.EditCartProductView.as_view(),name="cart edit"),
    path("cart/delete/<str:id>/",views.DeleteCartProductView.as_view(),name="cart delete"),
    path("category/",views.CategoriesListView.as_view(),name="category list"),
    path("category/<str:id>/",views.CategoryProductListView.as_view(),name="category id"),
    path("cart/count/",views.CartProductsCountView.as_view(),name="cart count"),
    path("buynow/<str:id>/",views.BuyNowProductView.as_view(),name="buy now"),
    path("order/place/<str:id>/",views.PlaceOrderView.as_view(),name="order place"),
    path("order/list/",views.ListOrderView.as_view(),name="List orders"),
    path("order/delete/<str:id>/",views.DeleteOrderView.as_view(),name="delete orders"),
    path("product/cart/<str:id>/",views.CartProductView.as_view(),name="product cart")
    # path("dlview/",views.DLView.as_view(),name="dl view"),
]
