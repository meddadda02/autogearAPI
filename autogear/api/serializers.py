from rest_framework import serializers
from .models import Brand, Garage, Car, Image

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'



class CarSerializer(serializers.ModelSerializer):
    brand = serializers.CharField()
    garage = serializers.CharField()
    class Meta:
        model = Car
        fields = '__all__'

    def create(self, validated_data):
        brand_name = validated_data.pop('brand')
        garage_name = validated_data.pop('garage')
        brand, created = Brand.objects.get_or_create(name=brand_name)
        garage, created = Garage.objects.get_or_create(name=garage_name)
        car = Car.objects.create(brand=brand, garage=garage, **validated_data)
        return car
    

    def to_representation(self, instance):
        affiche = super().to_representation(instance)
        affiche['brand'] = BrandSerializer(instance.brand).data
        affiche['garage'] = GarageSerializer(instance.garage).data
        affiche['images'] = ImageSerializer(instance.images.all(),many=True) .data   
            
        return affiche