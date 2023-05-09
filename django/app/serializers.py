from app import models
from rest_framework import serializers



# classes
class UserProfileSerializer(serializers.ModelSerializer):
    """
        سریالایز کردن داده های موجودیت کاربر
    """
    class Meta:
        model = models.UserProfileModel
        fields = '__all__'
        
        
class ParkingSerializer(serializers.ModelSerializer):
    """
        سریالایز کردن داده های پارکینگ
    """
    class Meta:
        model = models.ParkingModel
        fields = '__all__'
        
        
class ParkingSpaceFloorSerializer(serializers.ModelSerializer):
    """
        سریالایز کردن داده های طبقه پارکینگ
    """
    class Meta:
        model = models.ParkingSpaceFloorModel
        fields = '__all__'
        
        
class ParkingSpaceRowSerializer(serializers.ModelSerializer):
    """
        سریالایز کردن داده های ردیف طبقه پارکینگ
    """
    class Meta:
        model = models.ParkingSpaceRowModel
        fields = '__all__'
        
        
class ParkingSpaceNumberSerializer(serializers.ModelSerializer):
    """
        سریالایز کردن داده های شماره جای پارک پارکینگ
    """
    class Meta:
        model = models.ParkingSpaceNumberModel
        fields = '__all__'
        
        
class TicketSerializer(serializers.ModelSerializer):
    """
        سریالایز کردن داده های بلیت
    """
    class Meta:
        model = models.TicketModel
        fields = '__all__'
        
        
class CreateTicketSerializer(serializers.Serializer):
    """
        سریالایز کردن داده های ساخت بلیت
    """
    driver_name = serializers.CharField(max_length = 25) # نام راننده
    driver_national_code = serializers.CharField(max_length = 10) # شماره ملی راننده
    driver_phone_number = serializers.CharField(max_length = 11) # شماره همراه راننده
    plate = serializers.CharField(max_length = 6) # پلاک ماشین
    parking_number = serializers.IntegerField() # شماره پارکینگ
    parking_row = serializers.IntegerField() # شماره ردیف
    parking_floor = serializers.CharField(max_length = 1) # نام طبقه