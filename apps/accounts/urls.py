from django.urls import path
from .views import *
from apps.order.views import *

app_name = 'accounts'

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('orders/',OrdersView.as_view(),name='orders'),
    path('profile/',ProfileUserView.as_view(),name='profile'),
    path('order/confirm/',ConfirmOrder.as_view(),name='confirm'),
    path('order/confirm/payment/',ConfirmPayment.as_view(),name='confirm-payment'),
    path('order/verify/',VerifyPaymentView.as_view(),name='verify-payment'),
]
