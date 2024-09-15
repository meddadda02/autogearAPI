from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.
fuel_ch = [
    ('diesel','Diesel'),
    ('gasoline', 'Gasoline'),
    ('hybrid', 'Hybrid'),
]
gearbox_ch=[
    ('automatique','Automatique'),
    ('manual', 'Manual'),
]
cartype_ch=[
    ('sedan','Sedan'),
    ('hatchback', 'Hatchback'),
    ('coupe','Coupe'),
    ('suv', 'Suv'),
    ('sport','Sport'),
]


class Brand(models.Model):
    name=models.CharField(max_length=100,blank=True)
    origin_country=models.CharField( max_length=100)
    def __str__(self):
        return f"{self.name} "

class Garage(models.Model):
    name=models.CharField(max_length=50,blank=True)
    adresse=models.CharField( max_length=100)
    phone=models.CharField(max_length=14)
    mail=models.EmailField(max_length=254)

    def __str__(self): 
       return f"{self.name} " 

class Car(models.Model):
    fuel=models.CharField(max_length=100,choices=fuel_ch)
    gearbox=models.CharField(max_length=100,choices=gearbox_ch)
    doors=models.IntegerField(validators=[MinValueValidator(2)])
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)])
    price=models.PositiveIntegerField()
    cartype=models.CharField(max_length=100,choices=cartype_ch)
    mealage=models.PositiveIntegerField()
    hp=models.PositiveIntegerField()
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    model=models.CharField(max_length=100)
    seats=models.PositiveIntegerField(validators=[MinValueValidator(2)])
    garage=models.ForeignKey(Garage,  on_delete=models.CASCADE)
    def __str__(self): 
        return f" {self.model} "
 

class Image(models.Model):
    image=models.ImageField(upload_to="media/")
    caption=models.CharField(max_length=500,blank=True)
    idcar=models.ForeignKey(Car, on_delete=models.CASCADE,related_name="images")
    def __str__(self):
        return f"{self.caption} "
    
