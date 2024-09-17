from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Car,Brand,Image,Garage
from .serializers import CarSerializer,BrandSerializer,ImageSerializer,GarageSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['GET','POST','DELETE'])
def List_cars(request):
    if request.method=="GET":
        cars = Car.objects.all()
        cars_serializer = CarSerializer(cars, many=True)
        return Response(cars_serializer.data)
    elif request.method == "POST":
        car_serializer = CarSerializer(data=request.data)
        if car_serializer.is_valid():
            car = car_serializer.save()
            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(idcar=car, image=image)
            return Response(car_serializer.data, status=status.HTTP_201_CREATED)
        return Response(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        Car.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def Car_detail(request,pk):
    try:
        car=Car.objects.get(id=pk)
        car_serializer=CarSerializer(car)
        return Response(car_serializer.data)
    except Car.DoesNotExist:
        return Response("your id "f"{pk}"" was not found",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['Get'])
def Car_cherche(request, ch):
    car = Car.objects.filter(brand__name=ch) | Car.objects.filter(model=ch)
    if car.exists():
        car_serializer = CarSerializer(car, many=True)
        return Response(car_serializer.data)
    else:
        return Response(f"{ch}"" was not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','POST'])
def List_brands(request):
    if request.method=='GET':
        brand=Brand.objects.all()
        brand_serializers=BrandSerializer(brand,many=True)
        return Response(brand_serializers.data)
    if request.method=='POST':
        brand_serializers=BrandSerializer(data=request.data)
        if brand_serializers.is_valid():
            brand=brand_serializers.save
            return Response(brand_serializers.data,status=status.HTTP_201_CREATED)
        return Response("invalid",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def Brand_detail(request,pk):
    try:
        brand=Brand.objects.get(id=pk)
        brand_serializers=BrandSerializer(brand)
        return Response(brand_serializers.data)
    except Brand.DoesNotExist:
        return Response("your id "f"{pk}"" was not found",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def List_garage(request):
    if request.method=='GET':
        garage=Garage.objects.all()
        garage_serializers=GarageSerializer(garage,many=True)
        return Response(garage_serializers.data)
    if request.method=='POST':
        garage_serializers=GarageSerializer(data=request.data)
        if garage_serializers.is_valid():
            garage=garage_serializers.save()
            return Response(garage_serializers.data,status=status.HTTP_201_CREATED)
        return Response("invalid",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def Garage_detail(request,pk):
    try:
        garage=Garage.objects.get(id=pk)
        garage_serializers=GarageSerializer(garage)
        return Response(garage_serializers.data)
    except Garage.DoesNotExist:
        return Response("your id "f"{pk}"" was not found",status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'POST'])
def List_image(request):
    if request.method == 'GET':
        images = Image.objects.all()
        image_serializers = ImageSerializer(images, many=True)
        return Response(image_serializers.data)

    if request.method == 'POST':
        car_id = request.data.get('car_id')

        if not car_id:
            return Response({"error": "Car ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        car = get_object_or_404(Car, id=car_id)

        if 'image_file' not in request.FILES:
            return Response({"error": "Image file is required"}, status=status.HTTP_400_BAD_REQUEST)
        image_data = {'image': request.FILES['image_file'], 'idcar': car.id}
        image_serializers = ImageSerializer(data=image_data)

        if image_serializers.is_valid():
            image_serializers.save()
            return Response(image_serializers.data, status=status.HTTP_201_CREATED)

        return Response(image_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def Image_detail(request,pk):
    try:
        image=Image.objects.get(id=pk)
        image_serializers=ImageSerializer(image)
        return Response(image_serializers.data)
    except Image.DoesNotExist:
        return Response("your id "f"{pk}"" was not found",status=status.HTTP_400_BAD_REQUEST)
    
