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
]