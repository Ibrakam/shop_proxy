from django.urls import path
from . import views

urlpatterns = [
    path('send-cart/', views.send_data_to_octo, name='send_cart_to_octo'),
]
