from app import models
from rest_framework import serializers


# classes
class UserProfileSerializer(serializers.ModelSerializer):
    """
        سریالایز کردن داده های موجودیت کاربر
    """
    class Meta:
        """
            کلاسی برای دادن اطلاعات به جنگو رست
        """
        model = models.UserProfileModel  # مدل استفاده شده برای سریالایزر کردن داده ها (کاربر)
        fields = ['id','first_name', 'last_name', 'mobile_number', 'password']  # فیلدهایی که داده انها سریالایز میشود 
        extra_kwargs = { 
            'password':{'write_only': True},
            'first_name':{'required':False},
            'last_name':{'required':False}
            }