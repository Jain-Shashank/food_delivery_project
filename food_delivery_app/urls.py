# food_delivery_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('user-details/', user_details, name='user_details'),
    path('monthly-status/', monthly_status, name='monthly_status'),
]
