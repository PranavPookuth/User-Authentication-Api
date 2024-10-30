from tkinter.font import names
from .import views
from django.urls import path
from .views import *


urlpatterns = [

    # login register logout

    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/<int:pk>/',Userdetails.as_view(),name='user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('category/',Categorycreateview.as_view(),name='category'),
    path('category/<int:pk>/',Categorydetails.as_view(),name='category_details'),
    path('products/',Productcreateview.as_view(),name='products'),
    path('products/<int:pk>/',Productdetails.as_view(),name='products_details'),
    path('customer/',Customercreateview.as_view(),name='customer'),
    path('customer/<int:pk>/',Customerdetails.as_view(),name='customer_details'),
    path('orders/', Ordercreateview.as_view(), name='orders'),
    path('orders/<int:pk>/', Orderdetails.as_view(), name='Order_details'),

]