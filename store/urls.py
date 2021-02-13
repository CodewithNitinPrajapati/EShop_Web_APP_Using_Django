from django.contrib import admin
from django.urls import path
from .views import Login,Signup,Index,logout,Cart,CheckOut,OrderView


urlpatterns = [
    #path('',Index.as_view(),name='Home'),
    path('', Index.as_view(), name='Home'),
    path('Signup', Signup.as_view(), name='Signup'),
    path('Login',Login.as_view(), name='Login'),
    path('Logout',logout, name='Logout'),
    path('cart',Cart.as_view(), name='Cart'),
    path('check-out', CheckOut.as_view(), name='chackout'),
    path('orders', OrderView.as_view(), name='orderview'),

]