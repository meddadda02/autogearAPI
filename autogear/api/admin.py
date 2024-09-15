from django.contrib import admin
from .models import Brand,Garage,Car,Image

# Register your models here.
admin.site.register(Brand)
admin.site.register(Garage)
admin.site.register(Car)
admin.site.register(Image)