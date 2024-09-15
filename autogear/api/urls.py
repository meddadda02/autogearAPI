# urls.py

from django.urls import path
from .views import *
urlpatterns = [
    path('cars/', List_cars, name='car_create'), 
    path('cars/<int:pk>/',Car_detail,name='car_detail'), 
    path('cars/<str:ch>/',Car_cherche,name="car_chercher"),
    
    path('brands/', List_brands, name='brand_create'), 
    path('brands/<int:pk>/',Brand_detail,name='brand_detail'), 
    
    path('garage/', List_garage, name='garage_create'), 
    path('garage/<int:pk>/',Garage_detail,name='garage_detail'), 
  
    path('images/', List_image, name='image_create'), 
    path('images/<int:pk>/',Image_detail,name='image_detail'),
]
