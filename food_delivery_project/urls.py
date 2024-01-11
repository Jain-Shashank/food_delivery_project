# food_delivery_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('food-delivery/', include('food_delivery_app.urls')),
]
